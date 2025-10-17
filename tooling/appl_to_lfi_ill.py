import argparse
import sys
import os
import importlib.util
import appl_ast
import lfi_ill

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
            return lfi_ill.String("[]") # Simplification

        elif isinstance(appl_node, appl_ast.Cons):
            head = self.compile(appl_node.head)
            tail = self.compile(appl_node.tail)
            return lfi_ill.TensorPair(head, tail) # Simplification

        else:
            raise NotImplementedError(f"APPL node type not yet supported: {type(appl_node)}")

    def compile_type(self, type_):
        """
        Translates APPL types to LFI ILL types.
        """
        return str(type_)

def main():
    parser = argparse.ArgumentParser(description="Compile APPL code to LFI ILL.")
    parser.add_argument("file", help="The APPL file to compile (as a Python file).")
    args = parser.parse_args()

    try:
        module_name = os.path.splitext(os.path.basename(args.file))[0]
        spec = importlib.util.spec_from_file_location(module_name, args.file)
        appl_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(appl_module)
        appl_ast_node = appl_module.APPL_AST
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        return
    except Exception as e:
        print(f"Error loading APPL module from file: {e}")
        return

    compiler = ApplToLfiIllCompiler()
    lfi_ill_ast = compiler.compile(appl_ast_node.term)

    print("--- COMPILED LFI ILL AST ---")
    print(repr(lfi_ill_ast))

    output_filename = args.file.replace(".py", ".lfi_ill")
    with open(output_filename, 'w') as f:
        f.write(repr(lfi_ill_ast))

    print(f"\nSuccessfully compiled to {output_filename}")


if __name__ == "__main__":
    main()