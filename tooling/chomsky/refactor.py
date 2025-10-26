"""
A tool for refactoring Python code to move it down the Chomsky hierarchy.

This module provides the core logic for the "decidable refactoring" tool. It
uses the `ast` module to perform transformations on the Abstract Syntax Tree
of a Python file, with the primary goal of converting functions with general
recursion into provably terminating versions.
"""

import ast
from tooling.chomsky.analyzer import CodeAnalyzer

class GeneralToPrimitiveTransformer(ast.NodeTransformer):
    """
    An AST transformer that converts a general recursive function to a
    primitive recursive one by adding a 'fuel' parameter.
    """

    def __init__(self, func_name):
        self.func_name = func_name

    def visit_FunctionDef(self, node):
        if node.name == self.func_name:
            # Add the 'fuel' parameter
            node.args.args.append(ast.arg(arg="fuel"))

            # Add the fuel check at the beginning of the function
            fuel_check = ast.If(
                test=ast.Compare(
                    left=ast.Name(id="fuel", ctx=ast.Load()),
                    ops=[ast.Eq()],
                    comparators=[ast.Constant(value=0)],
                ),
                body=[ast.Return(value=ast.Constant(value=None))],
                orelse=[],
            )
            node.body.insert(0, fuel_check)

            # Visit the rest of the function's body
            self.generic_visit(node)
        return node

    def visit_Call(self, node):
        # First, visit the children of the node to handle nested calls from the inside out.
        self.generic_visit(node)

        if isinstance(node.func, ast.Name) and node.func.id == self.func_name:
            # Add the fuel decrement to recursive calls
            node.args.append(
                ast.BinOp(
                    left=ast.Name(id="fuel", ctx=ast.Load()),
                    op=ast.Sub(),
                    right=ast.Constant(value=1),
                )
            )
        return node

class CodeRefactorer:
    """
    A class to perform AST-based refactorings on Python code.
    """

    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)

    def refactor_to_decidable(self):
        """
        Refactors all general recursive functions in the code to be decidable.
        """
        analyzer = CodeAnalyzer(self.source_code)
        analysis = analyzer.analyze()

        for func_name, func_analysis in analysis.items():
            if func_analysis["recursion_type"] == "general":
                transformer = GeneralToPrimitiveTransformer(func_name)
                self.tree = transformer.visit(self.tree)

        return ast.unparse(self.tree)
