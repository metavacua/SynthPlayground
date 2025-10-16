from aura_lang import ast
import re
import json

# --- Object System ---

class Object:
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"Object(value={self.value})"

class Integer(Object): pass
class String(Object): pass
class Boolean(Object): pass
class ReturnValue(Object): pass

class Function(Object):
    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

class Builtin(Object):
    def __init__(self, fn):
        self.fn = self.value = fn

class Environment:
    def __init__(self, outer=None):
        self.store, self.outer = {}, outer
    def get(self, name):
        val = self.store.get(name)
        return val if val is not None else self.outer.get(name) if self.outer else None
    def set(self, name, val):
        self.store[name] = val
        return val

# --- Agent Tooling Bridge ---

# --- Agent Tooling Bridge ---

def _placeholder_agent_call_tool(tool_name, *args):
    """
    Placeholder for calling the agent's real tools.
    This will be replaced by a real implementation provided by the executor.
    """
    print(f"[Aura Interpreter]: Tool call to '{tool_name}' with args {args} is not yet implemented.")
    if tool_name == "hdl_prover.prove_sequent":
        # Return a mock value for now
        return True
    return None

# This can be overwritten by the executor.
# By default, it's a placeholder. The aura_executor.py script
# will replace this with a real implementation.
agent_call_tool = _placeholder_agent_call_tool

# --- Interpreter ---

def evaluate(node, env):
    node_type = type(node)
    if node_type == ast.Program: return eval_program(node, env)
    elif node_type == ast.ExpressionStatement: return evaluate(node.expression, env)
    elif node_type == ast.LetStatement:
        val = evaluate(node.value, env)
        env.set(node.name.value, val)
    elif node_type == ast.ReturnStatement: return ReturnValue(evaluate(node.value, env))
    elif node_type == ast.BlockStatement: return eval_block_statement(node, env)
    elif node_type == ast.FunctionDefinition: env.set(node.name.value, Function(node.params, node.body, env))
    elif node_type == ast.IfStatement: return eval_if_statement(node, env)
    elif node_type == ast.ForStatement: return eval_for_statement(node, env)
    elif node_type == ast.PrintStatement: return eval_print_statement(node, env)
    elif node_type == ast.IntegerLiteral: return Integer(node.value)
    elif node_type == ast.StringLiteral: return String(node.value)
    elif node_type == ast.BooleanLiteral: return Boolean(node.value)
    elif node_type == ast.Identifier: return eval_identifier(node, env)
    elif node_type == ast.ListLiteral: return Object(eval_expressions(node.elements, env))
    elif node_type == ast.InfixExpression:
        left, right = evaluate(node.left, env), evaluate(node.right, env)
        if node.operator == 'in' and isinstance(right, String):
            # The 'in' operator returns a raw boolean, not an Object, for the if statement.
            return left.value in right.value
        return eval_infix_expression(node.operator, left, right)
    elif node_type == ast.CallExpression:
        function = evaluate(node.function, env)
        args = eval_expressions(node.arguments, env)
        return apply_function(function, args)
    elif node_type == ast.MemberAccess:
        obj = evaluate(node.object, env)
        prop_name = node.property.value
        target = obj.value if isinstance(obj, Object) else obj
        return getattr(target, prop_name, None)
    return None

def eval_program(program, env):
    result = None  # Initialize result
    for statement in program.statements:
        result = evaluate(statement, env)
        if isinstance(result, ReturnValue):
            return result.value
    # If the script ends without an expression (e.g. only let statements),
    # result can be None. We should return a proper Aura Object for consistency.
    if result is None:
        return Object(None)
    return result

def eval_block_statement(block, env):
    for statement in block.statements:
        result = evaluate(statement, env)
        if isinstance(result, ReturnValue): return result
    return result

def _is_truthy(obj) -> bool:
    """
    Determines the truthiness of an Aura object, handling raw Python types as well.
    - None and False are falsy.
    - Aura Booleans are evaluated by their value.
    - Numbers are falsy if 0.
    - Strings and lists are falsy if empty.
    - All other objects are truthy.
    """
    if obj is None:
        return False
    if isinstance(obj, bool): # Handle raw bools that might slip through
        return obj

    val = obj.value
    if isinstance(val, bool):
        return val
    if val is None:
        return False
    if isinstance(val, (int, float)):
        return val != 0
    if isinstance(val, (str, list, dict)):
        return len(val) > 0
    return True # All other object values are considered truthy

def eval_if_statement(node, env):
    condition_obj = evaluate(node.condition, env)

    if _is_truthy(condition_obj):
        return evaluate(node.consequence, env)
    elif node.alternative:
        return evaluate(node.alternative, env)
    else:
        # If there's no 'else' block, an 'if' statement evaluates to null.
        return Object(None)

def eval_for_statement(node, env):
    iterable_obj = evaluate(node.iterable, env)
    loop_env = Environment(outer=env)
    for item in iterable_obj.value:
        loop_env.set(node.identifier.value, Integer(item) if isinstance(item, int) else Object(item))
        evaluate(node.body, loop_env)

def eval_print_statement(node, env):
    evaluated_obj = evaluate(node.value, env)
    value_to_print = None

    if hasattr(evaluated_obj, 'value'):
        value_to_print = evaluated_obj.value
    else:
        # This handles cases where a raw value might be returned (e.g. from 'in' operator)
        value_to_print = evaluated_obj

    if isinstance(value_to_print, dict):
        print(json.dumps(value_to_print, indent=2))
    else:
        print(value_to_print)

def eval_infix_expression(op, left, right):
    """Handles infix operations like +, -, ==, etc."""
    # Ensure both left and right are Aura objects and have a .value attribute
    if not isinstance(left, Object) or not isinstance(right, Object):
         # This case should ideally not be hit if the parser is correct
        return Boolean(False)

    l_val = left.value
    r_val = right.value

    # Generic equality checks should be handled first and for all types.
    if op == '==':
        return Boolean(l_val == r_val)
    if op == '!=':
        return Boolean(l_val != r_val)

    # Type-specific operations.
    # Using `type()` is important here to avoid `isinstance(True, int)` being true.
    if type(l_val) is int and type(r_val) is int:
        if op == '+': return Integer(l_val + r_val)
        if op == '-': return Integer(l_val - r_val)
        if op == '*': return Integer(l_val * r_val)
        if op == '/': return Integer(l_val // r_val)
        # Any other operator is invalid for two integers.
        return Object(None)

    # Add other type-specific operations here in the future (e.g., string concat).

    return Object(None)  # Unsupported operator for the given types

def eval_identifier(node, env):
    return env.get(node.value) or BUILTINS.get(node.value)

def eval_expressions(exps, env): return [evaluate(e, env) for e in exps]

def apply_function(fn, args):
    if isinstance(fn, Function):
        extended_env = Environment(outer=fn.env)
        for param, arg in zip(fn.params, args): extended_env.set(param.value, arg)
        evaluated = evaluate(fn.body, extended_env)
        return evaluated.value if isinstance(evaluated, ReturnValue) else evaluated
    elif isinstance(fn, Builtin):
        # The arguments are already Aura Objects, so we can pass them directly.
        return fn.fn(*args)

class Agent(Object):
    def __init__(self):
        self.value = self
        self.call_tool = Builtin(agent_call_tool)

BUILTINS = {"agent": Agent()}