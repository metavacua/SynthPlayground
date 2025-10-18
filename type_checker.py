from appl_ast import *
from planning import *

class TypeCheckError(Exception):
    pass

class TypeChecker:
    def __init__(self):
        # The unrestricted context for variables that can be used multiple times.
        self.unrestricted_context = {}
        # The linear context for variables that must be used exactly once.
        self.linear_context = {}

    def type_check(self, term: Term) -> Type:
        if isinstance(term, (Int, TInt)):
            return TInt()
        elif isinstance(term, (String, TString)):
            return TString()
        elif isinstance(term, (Bool, TBool)):
            return TBool()
        elif isinstance(term, (Unit, TUnit)):
            return TUnit()
        elif isinstance(term, Var):
            if term.name in self.linear_context:
                # Consume the linear variable
                return self.linear_context.pop(term.name)
            elif term.name in self.unrestricted_context:
                return self.unrestricted_context[term.name]
            else:
                raise TypeCheckError(f"Variable '{term.name}' not found in context.")
        elif isinstance(term, Fun):
            # For functions, we add the variable to the context and check the body.
            # The type of the variable determines if it's linear or unrestricted.
            if isinstance(term.type, TExponential):
                self.unrestricted_context[term.var] = term.type.t
            else:
                self.linear_context[term.var] = term.type

            body_type = self.type_check(term.body)
            return TFun(term.type, body_type)
        elif isinstance(term, App):
            fun_type = self.type_check(term.f)
            arg_type = self.type_check(term.arg)

            if not isinstance(fun_type, TFun):
                raise TypeCheckError(f"Cannot apply a non-function type: {fun_type}")

            if fun_type.t1 != arg_type:
                raise TypeCheckError(f"Type mismatch in function application. Expected {fun_type.t1}, got {arg_type}")

            return fun_type.t2
        elif isinstance(term, Pair):
            t1 = self.type_check(term.e1)
            t2 = self.type_check(term.e2)
            return TProd(t1, t2)
        elif isinstance(term, LetPair):
            pair_type = self.type_check(term.e1)
            if not isinstance(pair_type, TProd):
                raise TypeCheckError(f"Expected a product type, but got {pair_type}")

            self.linear_context[term.v1] = pair_type.t1
            self.linear_context[term.v2] = pair_type.t2

            return self.type_check(term.e2)
        elif isinstance(term, Let):
            t1 = self.type_check(term.e1)
            self.linear_context[term.var] = t1
            return self.type_check(term.e2)
        elif isinstance(term, Inl):
            t = self.type_check(term.e)
            return TSum(t, term.t_right)
        elif isinstance(term, Inr):
            t = self.type_check(term.e)
            return TSum(term.t_left, t)
        elif isinstance(term, Case):
            sum_type = self.type_check(term.e)
            if not isinstance(sum_type, TSum):
                raise TypeCheckError(f"Expected a sum type, but got {sum_type}")

            # Type check the 'inl' branch
            self.linear_context[term.v1] = sum_type.t1
            t1 = self.type_check(term.e1)

            # Type check the 'inr' branch
            self.linear_context[term.v2] = sum_type.t2
            t2 = self.type_check(term.e2)

            if t1 != t2:
                raise TypeCheckError(f"Type mismatch in case branches. Got {t1} and {t2}")

            return t1
        elif isinstance(term, Promote):
            # To promote an expression, it must be typeable in an empty linear context.
            # This is a simplification; a more complete implementation would handle this differently.
            original_linear_context = self.linear_context
            self.linear_context = {}
            t = self.type_check(term.e)
            if self.linear_context:
                raise TypeCheckError("Cannot promote an expression that uses linear variables.")
            self.linear_context = original_linear_context
            return TExponential(t)
        elif isinstance(term, LetBang):
            e1_type = self.type_check(term.e1)
            if not isinstance(e1_type, TExponential):
                raise TypeCheckError(f"Expected an exponential type, but got {e1_type}")

            self.unrestricted_context[term.v] = e1_type.t
            return self.type_check(term.e2)
        elif isinstance(term, AST):
            return TTerm()
        elif isinstance(term, Nil):
            return TList(term.type)
        elif isinstance(term, Cons):
            head_type = self.type_check(term.head)
            tail_type = self.type_check(term.tail)
            if not isinstance(tail_type, TList):
                raise TypeCheckError("Tail of a cons must be a list.")
            if head_type != tail_type.t:
                raise TypeCheckError(f"Type mismatch in cons. Head is {head_type}, but tail is {tail_type}")
            return TList(head_type)
        else:
            raise NotImplementedError(f"Type checking not implemented for {type(term).__name__}")

def type_check(term: Term, unrestricted_context: dict = None, linear_context: dict = None) -> Type:
    """
    Type-checks the given term in the provided contexts.
    """
    checker = TypeChecker()

    default_unrestricted_context = {
        'load_domain': TFun(TString(), TExponential(TUnit())),
        'create_state': TFun(TList(TString()), TExponential(TState())),
        'apply_action': TFun(TString(), TExponential(TState())),
        'is_goal': TFun(TList(TString()), TBool()),
        'get_current_state': TFun(TUnit(), TList(TString())),
        'parse': TFun(TString(), TTerm()),
        'unparse': TFun(TTerm(), TString()),
        'eval': TFun(TTerm(), TTerm()), # This is a simplification
    }

    if unrestricted_context:
        default_unrestricted_context.update(unrestricted_context)

    checker.unrestricted_context = default_unrestricted_context
    if linear_context:
        checker.linear_context = linear_context.copy()

    result = checker.type_check(term)
    if checker.linear_context:
        raise TypeCheckError(f"Unused linear variables: {', '.join(checker.linear_context.keys())}")
    return result