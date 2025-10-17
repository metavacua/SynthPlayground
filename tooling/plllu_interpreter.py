import sys
import os
from enum import Enum
from collections import Counter

# Ensure the project root is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class LogicValue(Enum):
    TRUE = 1
    FALSE = 0
    BOTH = 2  # t and f
    NEITHER = 3 # neither t nor f

class InterpretationError(Exception):
    """Custom exception for errors during interpretation."""
    pass

class FourValuedInterpreter:
    """
    Interprets a pLLLU AST using a four-valued logic (TRUE, FALSE, BOTH, NEITHER).
    It also enforces the linear consumption of resources from a given context.
    """
    def __init__(self, context):
        """
        Initializes the interpreter with a context.
        The context is a dictionary mapping atoms to their four-valued truth value.
        e.g., {'A': LogicValue.TRUE, 'B': LogicValue.BOTH}
        """
        self.context = context
        self.used_atoms = Counter()
        self.max_usage = Counter({atom: 1 for atom in context})

    def interpret(self, ast_node):
        """
        Main entry point for interpreting an AST.
        Verifies resource consumption after evaluation.
        """
        result = self._evaluate(ast_node)

        if self.used_atoms != self.max_usage:
            raise InterpretationError(
                f"Linearity Error: Context resources do not match consumption. "
                f"Required: {dict(self.max_usage)}, Consumed: {dict(self.used_atoms)}"
            )
        return result

    def _evaluate(self, node):
        """Dispatcher for AST node types."""
        node_type = node[0]
        if node_type == 'atom':
            return self._eval_atom(node)
        elif node_type == 'unary_op':
            return self._eval_unary_op(node)
        elif node_type == 'binary_op':
            return self._eval_binary_op(node)
        else:
            raise NotImplementedError(f"Unknown node type: {node_type}")

    def _eval_atom(self, node):
        """Evaluates an atom by looking it up in the context."""
        _, atom_name = node
        if atom_name not in self.context:
            raise InterpretationError(f"Atom '{atom_name}' not in context.")

        self.used_atoms[atom_name] += 1
        if self.used_atoms[atom_name] > self.max_usage[atom_name]:
            raise InterpretationError(f"Linearity Error: Atom '{atom_name}' consumed more than once.")

        return self.context[atom_name]

    def _eval_unary_op(self, node):
        """Evaluates a unary operation."""
        _, op, child = node
        val = self._evaluate(child)

        if op == '~': # Undeterminedness (LFU)
            if val == LogicValue.TRUE: return LogicValue.FALSE
            if val == LogicValue.FALSE: return LogicValue.TRUE
            if val == LogicValue.BOTH: return LogicValue.BOTH
            if val == LogicValue.NEITHER: return LogicValue.NEITHER

        if op == '∘': # Consistency (LFI)
            if val == LogicValue.TRUE or val == LogicValue.FALSE:
                return LogicValue.TRUE
            else: # BOTH or NEITHER
                return LogicValue.FALSE

        if op == '!': # For now, ! is transparent. A real implementation would be more complex.
            return val

        raise NotImplementedError(f"Unary operator '{op}'")

    def _eval_binary_op(self, node):
        """Evaluates a binary operation using four-valued truth tables."""
        _, op, left, right = node

        # Additive operators (&, |) duplicate the context for each branch.
        if op == '&' or op == '|':
            initial_used_atoms = self.used_atoms.copy()

            # Evaluate left branch, ensuring context is reset even if it fails
            try:
                l_val = self._evaluate(left)
                left_used_atoms = self.used_atoms.copy()
            finally:
                self.used_atoms = initial_used_atoms

            # Evaluate right branch from the same initial state
            r_val = self._evaluate(right)
            right_used_atoms = self.used_atoms.copy()

            # For additives, the resources consumed by both branches must be identical.
            if left_used_atoms != right_used_atoms:
                raise InterpretationError(
                    f"Linearity Error for additive operator '{op}': branches consume different resources. "
                    f"Left consumed: {dict(left_used_atoms - initial_used_atoms)}, "
                    f"Right consumed: {dict(right_used_atoms - initial_used_atoms)}"
                )

            # The final usage is the usage of one of the identical branches.
            self.used_atoms = left_used_atoms

            if op == '&': # Conjunction (meet)
                if l_val == LogicValue.FALSE or r_val == LogicValue.FALSE: return LogicValue.FALSE
                if l_val == LogicValue.TRUE: return r_val
                if r_val == LogicValue.TRUE: return l_val
                if l_val == LogicValue.NEITHER or r_val == LogicValue.NEITHER: return LogicValue.NEITHER
                return LogicValue.BOTH

            if op == '|': # Disjunction (join)
                if l_val == LogicValue.TRUE or r_val == LogicValue.TRUE: return LogicValue.TRUE
                if l_val == LogicValue.FALSE: return r_val
                if r_val == LogicValue.FALSE: return l_val
                if l_val == LogicValue.BOTH or r_val == LogicValue.BOTH: return LogicValue.BOTH
                return LogicValue.NEITHER

        if op == '-o': # Implication
            # NOTE: This is a truth-functional simplification and is NOT a correct
            # implementation of linear implication, which requires modifying the
            # context for the sub-evaluation (i.e., Gamma, A |- B).
            # This implementation incorrectly treats it as a multiplicative, consuming
            # resources for both sub-formulas from the same context.
            l_val = self._evaluate(left)
            r_val = self._evaluate(right)

            # Truth table for A -> B based on (~A | B)
            neg_l_val = {
                LogicValue.TRUE: LogicValue.FALSE,
                LogicValue.FALSE: LogicValue.TRUE,
                LogicValue.BOTH: LogicValue.BOTH,
                LogicValue.NEITHER: LogicValue.NEITHER,
            }[l_val]

            if neg_l_val == LogicValue.TRUE or r_val == LogicValue.TRUE: return LogicValue.TRUE
            if neg_l_val == LogicValue.FALSE: return r_val
            if r_val == LogicValue.FALSE: return neg_l_val
            if neg_l_val == LogicValue.BOTH or r_val == LogicValue.BOTH: return LogicValue.BOTH
            return LogicValue.NEITHER

        raise NotImplementedError(f"Binary operator '{op}'")


# --- Self-test for demonstration ---
if __name__ == '__main__':
    from tooling.pda_parser import parse_formula

    print("--- Testing the pLLLU Four-Valued Interpreter ---")

    test_cases = [
        {"desc": "LFI: Consistency of TRUE is TRUE", "context": {'A': LogicValue.TRUE}, "formula": "∘A", "expected": LogicValue.TRUE},
        {"desc": "LFI: Consistency of BOTH is FALSE", "context": {'A': LogicValue.BOTH}, "formula": "∘A", "expected": LogicValue.FALSE},
        {"desc": "LFU: Undeterminedness of TRUE is FALSE", "context": {'A': LogicValue.TRUE}, "formula": "~A", "expected": LogicValue.FALSE},
        {"desc": "LFU: Undeterminedness of BOTH is BOTH", "context": {'A': LogicValue.BOTH}, "formula": "~A", "expected": LogicValue.BOTH},
        {"desc": "Linearity: Valid consumption", "context": {'A': LogicValue.TRUE, 'B': LogicValue.FALSE}, "formula": "A & B", "expected": LogicValue.FALSE},
        {"desc": "Linearity: Fails on reuse", "context": {'A': LogicValue.TRUE}, "formula": "A & A", "should_fail": True},
        {"desc": "Linearity: Fails on non-consumption", "context": {'A': LogicValue.TRUE, 'B': LogicValue.TRUE}, "formula": "A", "should_fail": True},
    ]

    for case in test_cases:
        print(f"\n--- Running Test: {case['desc']} ---")
        try:
            ast = parse_formula(case['formula'])
            interpreter = FourValuedInterpreter(case['context'])
            result = interpreter.interpret(ast)

            if case.get('should_fail'):
                print(f"FAILURE: Should have failed but returned {result.name}")
            elif result == case['expected']:
                print(f"SUCCESS: Returned {result.name} as expected.")
            else:
                print(f"FAILURE: Expected {case['expected'].name} but got {result.name}")

        except (InterpretationError, NotImplementedError) as e:
            if case.get('should_fail'):
                print(f"SUCCESS: Correctly failed with error: {e}")
            else:
                print(f"FAILURE: Should have passed but failed with error: {e}")
        except Exception as e:
            print(f"UNEXPECTED ERROR: {e}")