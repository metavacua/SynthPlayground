import ast
import re
import argparse
import textwrap
import os
import black
import subprocess
import shlex


class PLangSyntaxError(Exception):
    pass


class PLangTransformer(ast.NodeTransformer):
    """
    Transforms the special P-Lang AST nodes into standard Python AST nodes.
    """

    def __init__(self):
        super().__init__()
        self.runtime_imported = False

    def _handle_dialetheia(self, node):
        """Transforms a __plang_dialetheia__ call into a ParaconsistentVariable instantiation."""
        self.runtime_imported = True
        var_name_node = node.args[0]
        dict_str_node = node.args[1]
        var_name = var_name_node.value
        dict_str = dict_str_node.value

        try:
            dict_node = ast.parse(dict_str, mode="eval").body
            if not isinstance(dict_node, ast.Dict):
                raise PLangSyntaxError(
                    "Dialetheia block did not resolve to a dictionary."
                )
            for key in dict_node.keys:
                if not isinstance(key, ast.Constant) or not isinstance(key.value, str):
                    raise PLangSyntaxError(
                        "Invalid key in dialetheia block. All stance keys must be quoted strings."
                    )
        except SyntaxError:
            raise PLangSyntaxError(f"Invalid syntax in dialetheia block: {dict_str}")

        constructor_call = ast.Call(
            func=ast.Name(id="ParaconsistentVariable", ctx=ast.Load()),
            args=[dict_node],
            keywords=[],
        )

        return ast.Assign(
            targets=[ast.Name(id=var_name, ctx=ast.Store())], value=constructor_call
        )

    def _handle_resolve(self, node):
        """Transforms a __plang_resolve__ call into a .resolve() method call."""
        var_name_node = node.args[0]
        stance_expr_node = node.args[1]
        var_name = var_name_node.value

        return ast.Call(
            func=ast.Attribute(
                value=ast.Name(id=var_name, ctx=ast.Load()),
                attr="resolve",
                ctx=ast.Load(),
            ),
            args=[stance_expr_node],
            keywords=[],
        )

    def _handle_resolve_policy(self, node):
        """Transforms a __plang_resolve_policy__ call by invoking the decider."""
        component_dir_node = node.args[0]
        policy_path_node = node.args[1]
        component_dir = component_dir_node.value
        policy_path = policy_path_node.value

        print("\n--- Invoking Decider Engine from Transpiler ---")
        decider_script = os.path.join(os.path.dirname(__file__), "decider.py")
        command = f"python3 {decider_script} {component_dir} --policy {policy_path}"

        try:
            result = subprocess.run(
                shlex.split(command),
                check=True,
                capture_output=True,
                text=True,
            )
            print(result.stdout)
            winner_path = None
            for line in result.stdout.split("\n"):
                if line.strip().startswith("-> Winning artifact:"):
                    winner_path = line.split(":", 1)[1].strip()
                    break
            if not winner_path:
                raise PLangSyntaxError("Decider did not report a winning artifact.")
            print(f"--- Decider Engine Finished. Winner: {winner_path} ---\n")
            return ast.Constant(value=winner_path)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise PLangSyntaxError(f"Failed to execute decider engine: {e}")

    def visit_Module(self, node):
        node = self.generic_visit(node)
        if self.runtime_imported:
            import_node = ast.ImportFrom(
                module="toolchain.plang_runtime",
                names=[ast.alias(name="ParaconsistentVariable")],
                level=0,
            )
            node.body.insert(0, import_node)
        return node

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            return self.generic_visit(node)

        handler_map = {
            "__plang_dialetheia__": self._handle_dialetheia,
            "__plang_resolve__": self._handle_resolve,
            "__plang_resolve_policy__": self._handle_resolve_policy,
        }

        handler = handler_map.get(node.func.id)
        if handler:
            return handler(node)

        return self.generic_visit(node)


def preprocess_plang(source_code):
    """
    Uses regex to convert P-Lang syntax into valid Python syntax
    that the PLangTransformer can understand.
    """
    # Stance-based resolution
    source_code = re.sub(
        r"resolve\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+with\s+(?!policy)(.*)",
        r"__plang_resolve__('\1', \2)",
        source_code,
    )
    # Policy-based resolution
    source_code = re.sub(
        r"resolve\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+with\s+policy\s+(.*)",
        r"__plang_resolve_policy__('\1', \2)",
        source_code,
    )

    dialetheia_pattern = re.compile(
        r"dialetheia\s+([a-zA-Z_][a-zA-Z0-9_]*):\n((?:[ \t]+.*\n?)+)", re.MULTILINE
    )

    def dialetheia_repl(match):
        var_name = match.group(1)
        block_content = textwrap.dedent(match.group(2)).strip()
        dict_str = f"{{{block_content}}}"
        return f"__plang_dialetheia__('{var_name}', '''{dict_str}''')"

    processed_code = dialetheia_pattern.sub(dialetheia_repl, source_code)

    return processed_code


def transpile_plang(source_path, output_path):
    """
    Reads a .plang file, transpiles it to Python, and writes the output.
    """
    print(f"Transpiling {source_path} to {output_path}...")

    with open(source_path, "r") as f:
        source_code = f.read()

    preprocessed_code = preprocess_plang(source_code)

    tree = ast.parse(preprocessed_code)
    transformer = PLangTransformer()
    transformed_tree = transformer.visit(tree)
    ast.fix_missing_locations(transformed_tree)
    unformatted_code = ast.unparse(transformed_tree)

    try:
        formatted_code = black.format_str(unformatted_code, mode=black.Mode())
        print("Successfully formatted transpiled code with black.")
    except black.NothingChanged:
        formatted_code = unformatted_code
        print("Transpiled code was already compliant with black formatting.")

    with open(output_path, "w") as f:
        f.write("# Transpiled from P-Lang\n\n")
        f.write(formatted_code)

    print("Transpilation successful.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transpile a .plang file to a .py file."
    )
    parser.add_argument("source", help="The path to the source .plang file.")
    parser.add_argument("output", help="The path to the destination .py file.")
    args = parser.parse_args()

    try:
        transpile_plang(args.source, args.output)
    except (PLangSyntaxError, FileNotFoundError) as e:
        if "PYTEST_CURRENT_TEST" not in os.environ:
            print(f"Error: {e}")
        exit(1)
