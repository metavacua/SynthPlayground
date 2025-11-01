import argparse
import ast
import sys

class DecidabilityRefactorer(ast.NodeTransformer):
    """
    Transforms a Python function with unbounded recursion (while loops)
    into a total function with a 'fuel' parameter and a control program.
    """

    def __init__(self, func_name):
        self.func_name = func_name
        self.transformed_func_name = f"{func_name}_total"
        self.is_in_target_func = False

    def visit_FunctionDef(self, node):
        if node.name == self.func_name:
            self.is_in_target_func = True

            # Save original details
            self.original_args = node.args

            # Create the new total function
            total_func_node = self._create_total_function(node)

            self.is_in_target_func = False
            return total_func_node
        return node

    def _create_total_function(self, original_node):
        # 1. Modify the function signature to accept 'fuel'
        new_args = ast.arguments(
            posonlyargs=[],
            args=[ast.arg(arg='fuel', annotation=None)] + original_node.args.args,
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[]
        )

        # 2. Transform the body
        transformed_body = [self.visit(n) for n in original_node.body]

        # 3. Create the new function definition
        total_func = ast.FunctionDef(
            name=self.transformed_func_name,
            args=new_args,
            body=transformed_body,
            decorator_list=[],
            returns=original_node.returns
        )
        return total_func

    def visit_While(self, node):
        if not self.is_in_target_func:
            return node

        # This is the core transformation: while -> if fuel > 0: ... recurse ...

        # 1. Create the fuel check
        fuel_check = ast.If(
            test=ast.Compare(
                left=ast.Name(id='fuel', ctx=ast.Load()),
                ops=[ast.Gt()],
                comparators=[ast.Constant(value=0)]
            ),
            body=[],
            orelse=[ast.Raise(
                exc=ast.Name(id='Exception', ctx=ast.Load()),
                cause=None
            )]
        )

        # 2. The body of the if is the original body of the while loop
        fuel_check.body.extend(node.body)

        # 3. Add the recursive call at the end of the if body
        recursive_call_args = [ast.BinOp(
            left=ast.Name(id='fuel', ctx=ast.Load()),
            op=ast.Sub(),
            right=ast.Constant(value=1)
        )] + [ast.Name(id=arg.arg, ctx=ast.Load()) for arg in self.original_args.args]

        recursive_call = ast.Return(
            value=ast.Call(
                func=ast.Name(id=self.transformed_func_name, ctx=ast.Load()),
                args=recursive_call_args,
                keywords=[]
            )
        )
        fuel_check.body.append(recursive_call)

        # We need to find what to return when the loop condition is false.
        # This is a hard problem. For now, let's assume the function returns the state.
        # This part requires more advanced analysis (what variables are the loop results?).
        # Simple solution: return the arguments.
        return_statement = ast.Return(value=ast.Name(id=self.original_args.args[0].arg, ctx=ast.Load()))

        # Replace the original while node with an if that checks the loop condition
        loop_condition_if = ast.If(
            test=node.test,
            body=[fuel_check],
            orelse=[return_statement] # If loop condition is false, return.
        )

        return loop_condition_if

def generate_control_program(func_name, total_func_name, total_func_code, fuel=100):
    """Generates the code for the control program."""
    control_code = f"""
# --- Transformed Total Function ---
{total_func_code}

# --- Control Program ---
def {func_name}_controller(initial_args, fuel={fuel}):
    try:
        print(f"Calling total function with fuel={{fuel}} and args={{initial_args}}")
        result = {total_func_name}(fuel, *initial_args)
        print(f"Computation finished naturally. Result: {{result}}")
        return result
    except Exception:
        print(f"Computation HALTED: Fuel exhausted at {fuel} iterations.")
        return None # Or some other indicator of failure

"""
    return control_code


def main():
    parser = argparse.ArgumentParser(description="Refactor a Python function to be decidable.")
    parser.add_argument("file_path", help="Path to the Python file containing the function.")
    parser.add_argument("func_name", help="The name of the function to refactor.")
    parser.add_argument("--fuel", type=int, default=100, help="Default fuel for the control program.")
    args = parser.parse_args()

    try:
        with open(args.file_path, 'r') as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        refactorer = DecidabilityRefactorer(args.func_name)
        transformed_tree = refactorer.visit(tree)

        # The transformed tree now contains the '_total' function.
        # We need to extract its source code.
        total_func_node = None
        for node in ast.walk(transformed_tree):
            if isinstance(node, ast.FunctionDef) and node.name == refactorer.transformed_func_name:
                total_func_node = node
                break

        if not total_func_node:
            raise ValueError(f"Function '{args.func_name}' not found or not transformed.")

        # A modern alternative to ast.unparse if not available
        import astor
        total_func_code = astor.to_source(total_func_node)

        control_program_code = generate_control_program(
            args.func_name,
            refactorer.transformed_func_name,
            total_func_code,
            args.fuel
        )

        print("--- Refactoring Complete ---")
        print("\nGenerated Code (Total Function + Control Program):\n")
        print(control_program_code)
        print("--------------------------")

    except FileNotFoundError:
        print(f"Error: File not found at {args.file_path}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred during refactoring: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
