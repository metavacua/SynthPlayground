import ast
import re
import argparse
import textwrap
import os
import black


class PLangSyntaxError(Exception):
    pass


class PLangTransformer(ast.NodeTransformer):
    """
    Transforms the special P-Lang AST nodes into standard Python AST nodes.
    """

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            return self.generic_visit(node)

        if node.func.id == "__plang_dialetheia__":
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
                    if not isinstance(key, ast.Constant) or not isinstance(
                        key.value, str
                    ):
                        raise PLangSyntaxError(
                            "Invalid key in dialetheia block. All stance keys must be quoted strings."
                        )

            except SyntaxError:
                raise PLangSyntaxError(
                    f"Invalid syntax in dialetheia block: {dict_str}"
                )

            assign_node = ast.Assign(
                targets=[ast.Name(id=var_name, ctx=ast.Store())], value=dict_node
            )
            return assign_node

        elif node.func.id == "__plang_resolve__":
            var_name_node = node.args[0]
            stance_expr_node = node.args[1]
            var_name = var_name_node.value

            subscript_node = ast.Subscript(
                value=ast.Name(id=var_name, ctx=ast.Load()),
                slice=stance_expr_node,
                ctx=ast.Load(),
            )
            return subscript_node

        return self.generic_visit(node)


def preprocess_plang(source_code):
    """
    Uses regex to convert P-Lang syntax into valid Python syntax
    that the PLangTransformer can understand.
    """
    dialetheia_pattern = re.compile(
        r"dialetheia\s+([a-zA-Z_][a-zA-Z0-9_]*):\n((?:[ \t]+.*\n?)+)", re.MULTILINE
    )

    def dialetheia_repl(match):
        var_name = match.group(1)
        block_content = textwrap.dedent(match.group(2)).strip()
        dict_str = f"{{{block_content}}}"
        return f"__plang_dialetheia__('{var_name}', '''{dict_str}''')"

    processed_code = dialetheia_pattern.sub(dialetheia_repl, source_code)

    resolve_pattern = re.compile(r"resolve\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+with\s+(.*)")

    def resolve_repl(match):
        var_name = match.group(1)
        stance_expr = match.group(2)
        return f"__plang_resolve__('{var_name}', {stance_expr})"

    processed_code = resolve_pattern.sub(resolve_repl, processed_code)

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

    # --- NEW: Format the output with black ---
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
