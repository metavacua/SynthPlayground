import ast
import json
import argparse
from tooling.witness_registry import WitnessRegistry

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.has_unbounded_while = False
        self.has_recursion = False
        self.function_defs = set()

    def visit_FunctionDef(self, node):
        self.function_defs.add(node.name)
        self.generic_visit(node)

    def visit_While(self, node):
        if isinstance(node.test, ast.Constant) and node.test.value is True:
            self.has_unbounded_while = True
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in self.function_defs:
            self.has_recursion = True
        self.generic_visit(node)

def classify_file(filepath, registry):
    with open(filepath, "r") as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    visitor = CodeVisitor()
    visitor.visit(tree)

    if visitor.has_unbounded_while:
        return registry.get_witness("recursive_and_re")
    elif visitor.has_recursion:
        return registry.get_witness("context_free")
    else:
        # This is a simplification. A real classifier would need to check for other
        # non-regular features. For now, we'll default to regular.
        return registry.get_witness("regular")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    args = parser.parse_args()

    registry = WitnessRegistry()
    registry.scan()

    classification = classify_file(args.file, registry)

    # We'll just print the name for the PoC
    print(f"Classification: {classification['name']}")

    with open("classification.json", "w") as f:
        json.dump(classification, f)
