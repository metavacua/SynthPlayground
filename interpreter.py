from appl_ast import (
    Term,
    Var,
    Int,
    String,
    Bool,
    Unit,
    Fun,
    App,
    Pair,
    LetPair,
    Let,
    Inl,
    Inr,
    Case,
    Promote,
    LetBang,
    Nil,
    Cons,
    AST,
)
from planning import (
    load_domain,
    create_state,
    apply_action,
    is_goal,
    get_current_state,
)
from parser import parse


class InterpError(Exception):
    pass


class Closure:
    def __init__(self, fun, env):
        self.fun = fun
        self.env = env


def _appl_to_python(val):
    if isinstance(val, String):
        return val.value
    elif isinstance(val, Int):
        return val.value
    elif isinstance(val, Bool):
        return val.value
    elif isinstance(val, (Cons, Nil)):
        return _appl_list_to_python_list(val)
    return val


def _appl_list_to_python_list(appl_list):
    py_list = []
    while isinstance(appl_list, Cons):
        py_list.append(_appl_to_python(appl_list.head))
        appl_list = appl_list.tail
    return py_list


def _python_list_to_appl_list(py_list: list) -> Term:
    """Converts a Python list of strings to an APPL list of strings."""
    result = Nil()
    for item in reversed(py_list):
        result = Cons(String(item), result)
    return result


class Primitive:
    def __init__(self, fun, arity):
        self.fun = fun
        self.arity = arity
        self.args = []

    def apply(self, arg):
        self.args.append(_appl_to_python(arg))
        if len(self.args) == self.arity:
            # Special handling for arity 0
            if self.arity == 0:
                return self.fun()
            return self.fun(*self.args)
        return self


class Interpreter:
    def __init__(self, env):
        self.env = env

    def interpret(self, term: Term) -> Term:
        if isinstance(term, (Int, String, Bool, Unit)):
            return term
        elif isinstance(term, Var):
            if term.name in self.env:
                return self.env[term.name]
            else:
                raise InterpError(f"Variable '{term.name}' not found in environment.")
        elif isinstance(term, Fun):
            return Closure(term, self.env)
        elif isinstance(term, App):
            fun_val = self.interpret(term.f)
            # Handle arity 0 functions
            if isinstance(fun_val, Primitive) and fun_val.arity == 0:
                return fun_val.fun()

            arg_val = self.interpret(term.arg)

            if isinstance(fun_val, Primitive):
                return fun_val.apply(arg_val)
            elif isinstance(fun_val, Closure):
                closure = fun_val
                new_env = closure.env.copy()
                new_env[closure.fun.var] = arg_val

                new_interpreter = Interpreter(new_env)
                return new_interpreter.interpret(closure.fun.body)
            else:
                raise InterpError("Cannot apply a non-function value.")
        elif isinstance(term, Pair):
            e1 = self.interpret(term.e1)
            e2 = self.interpret(term.e2)
            return Pair(e1, e2)
        elif isinstance(term, LetPair):
            pair_val = self.interpret(term.e1)
            if not isinstance(pair_val, Pair):
                raise InterpError("Expected a pair in let pair.")

            new_env = self.env.copy()
            new_env[term.v1] = pair_val.e1
            new_env[term.v2] = pair_val.e2

            new_interpreter = Interpreter(new_env)
            return new_interpreter.interpret(term.e2)
        elif isinstance(term, Let):
            val = self.interpret(term.e1)
            new_env = self.env.copy()
            new_env[term.var] = val
            new_interpreter = Interpreter(new_env)
            return new_interpreter.interpret(term.e2)
        elif isinstance(term, Inl):
            return Inl(self.interpret(term.e), term.t_right)
        elif isinstance(term, Inr):
            return Inr(self.interpret(term.e), term.t_left)
        elif isinstance(term, Case):
            sum_val = self.interpret(term.e)
            if not isinstance(sum_val, (Inl, Inr)):
                raise InterpError("Expected a sum in case.")

            new_env = self.env.copy()
            if isinstance(sum_val, Inl):
                new_env[term.v1] = sum_val.e
                new_interpreter = Interpreter(new_env)
                return new_interpreter.interpret(term.e1)
            else:  # Inr
                new_env[term.v2] = sum_val.e
                new_interpreter = Interpreter(new_env)
                return new_interpreter.interpret(term.e2)
        elif isinstance(term, Promote):
            return self.interpret(term.e)
        elif isinstance(term, LetBang):
            val = self.interpret(term.e1)

            new_env = self.env.copy()
            new_env[term.v] = val

            new_interpreter = Interpreter(new_env)
            return new_interpreter.interpret(term.e2)
        elif isinstance(term, Nil):
            return term
        elif isinstance(term, Cons):
            head = self.interpret(term.head)
            tail = self.interpret(term.tail)
            return Cons(head, tail)
        elif isinstance(term, AST):
            return term
        else:
            raise NotImplementedError(
                f"Interpretation not implemented for {type(term).__name__}"
            )


def _unparse(term: Term) -> str:
    # This is a simplified unparser. A more complete implementation would be needed for full homoiconicity.
    return repr(term)


def interpret(term: Term, env: dict = None) -> Term:
    """
    Interprets the given term in the provided environment.
    """
    default_env = {
        "load_domain": Primitive(load_domain, 1),
        "create_state": Primitive(create_state, 1),
        "apply_action": Primitive(apply_action, 1),
        "is_goal": Primitive(lambda goal_list: Bool(is_goal(goal_list)), 1),
        "get_current_state": Primitive(
            lambda: _python_list_to_appl_list(get_current_state()), 0
        ),
        "parse": Primitive(lambda s: AST(parse(s)), 1),
        "unparse": Primitive(lambda t: String(_unparse(t)), 1),
        "eval": Primitive(lambda t: interpret(t.term, env), 1),
    }
    if env:
        default_env.update(env)

    interpreter = Interpreter(default_env)
    return interpreter.interpret(term)
