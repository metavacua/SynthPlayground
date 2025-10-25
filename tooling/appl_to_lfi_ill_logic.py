import appl_ast
import lfi_ill


class ApplToLfiIllCompiler:
    def __init__(self):
        pass

    def compile(self, appl_node):
        """
        Recursively walks the APPL AST and translates it to an LFI ILL AST.
        """
        if isinstance(appl_node, appl_ast.Var):
            return lfi_ill.Var(appl_node.name)

        elif isinstance(appl_node, appl_ast.Int):
            return lfi_ill.Int(appl_node.value)

        elif isinstance(appl_node, appl_ast.Fun):
            var = self.compile(appl_node.var)
            type_ = self.compile_type(appl_node.type)
            body = self.compile(appl_node.body)
            return lfi_ill.Fun(var, type_, body)

        elif isinstance(appl_node, appl_ast.App):
            f = self.compile(appl_node.f)
            arg = self.compile(appl_node.arg)
            return lfi_ill.App(f, arg)

        elif isinstance(appl_node, appl_ast.Pair):
            e1 = self.compile(appl_node.e1)
            e2 = self.compile(appl_node.e2)
            return lfi_ill.TensorPair(e1, e2)

        elif isinstance(appl_node, appl_ast.LetPair):
            v1 = self.compile(appl_node.v1)
            v2 = self.compile(appl_node.v2)
            e1 = self.compile(appl_node.e1)
            e2 = self.compile(appl_node.e2)
            return lfi_ill.LetTensor(v1, v2, e1, e2)

        elif isinstance(appl_node, appl_ast.Promote):
            e = self.compile(appl_node.e)
            return lfi_ill.Promotion(e)

        elif isinstance(appl_node, appl_ast.LetBang):
            v = self.compile(appl_node.v)
            e1 = self.compile(appl_node.e1)
            e2 = self.compile(appl_node.e2)
            return lfi_ill.Dereliction(v, e1, e2)

        elif isinstance(appl_node, appl_ast.Inl):
            return lfi_ill.Inl(self.compile(appl_node.e))

        elif isinstance(appl_node, appl_ast.Inr):
            return lfi_ill.Inr(self.compile(appl_node.e))

        elif isinstance(appl_node, appl_ast.Case):
            e = self.compile(appl_node.e)
            v1 = self.compile(appl_node.v1)
            e1 = self.compile(appl_node.e1)
            v2 = self.compile(appl_node.v2)
            e2 = self.compile(appl_node.e2)
            return lfi_ill.Case(e, v1, e1, v2, e2)

        elif isinstance(appl_node, appl_ast.Unit):
            return lfi_ill.Unit()

        elif isinstance(appl_node, appl_ast.Nil):
            return lfi_ill.String("[]")  # Simplification

        elif isinstance(appl_node, appl_ast.Cons):
            head = self.compile(appl_node.head)
            tail = self.compile(appl_node.tail)
            return lfi_ill.TensorPair(head, tail)  # Simplification

        else:
            raise NotImplementedError(
                f"APPL node type not yet supported: {type(appl_node)}"
            )

    def compile_type(self, type_):
        """
        Translates APPL types to LFI ILL types.
        """
        return str(type_)
