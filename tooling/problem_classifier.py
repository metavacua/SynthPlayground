import ast
import json
import argparse
import sys
import os

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.witness_registry import WitnessRegistry

class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.has_unbounded_while = False
        self.has_recursion = False
        self.is_impure = False
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
        # A simple heuristic for impurity: calling 'open' is a side effect.
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            self.is_impure = True
        self.generic_visit(node)

def classify_file(filepath, registry, task_name=None):
    with open(filepath, "r") as f:
        source_code = f.read()

    has_todo = any(line.strip().startswith("# TODO:") for line in source_code.split('\n'))

    tree = ast.parse(source_code)
    visitor = CodeVisitor()
    visitor.visit(tree)

    classification = {}
    if has_todo:
        classification['problem_type'] = "Natural Language Task"

    # New logic for purity checking
    if task_name == "prove_purity" and visitor.is_impure:
        classification['problem_type'] = "Impurity Detected"

    # Determine the language class
    if visitor.has_unbounded_while:
        witness = registry.get_witness("recursive_and_re")
    elif visitor.has_recursion:
        witness = registry.get_witness("context_free")
    # A function with side effects isn't technically regular, but for this PoC
    # we will classify its *control flow* as regular.
    else:
        witness = registry.get_witness("regular")

    classification.update(witness)
    if 'name' in classification:
        classification['classification_name'] = classification.pop('name')

    return classification

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--task-name", required=True)
    parser.add_argument("--session-id", required=True)
    args = parser.parse_args()

    registry = WitnessRegistry()
    registry.scan()

    classification = classify_file(args.file, registry, args.task_name)

    print(json.dumps(classification))
