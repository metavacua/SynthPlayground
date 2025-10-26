"""
A constructive code analyzer for classifying Python code according to the Chomsky hierarchy.

This module provides the core logic for the "constructive" analysis of Python code.
It uses the `ast` module to parse Python code into an Abstract Syntax Tree (AST)
and then traverses the tree to identify key characteristics that determine the
computational complexity of the code.

The primary goal is to identify "witnesses" of decidability (e.g., primitive
recursion, bounded loops) and "counter-witnesses" (e.g., general recursion,
potential non-termination). This analysis provides the foundation for the
decidable refactoring toolchain.
"""

import ast
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from dbpedia_client import get_abstract

class CodeAnalyzer:
    """
    A class to analyze a Python AST and classify its components.
    """

    def __init__(self, source_code):
        self.source_code = source_code
        self.tree = ast.parse(source_code)
        self.analysis = {}

    def analyze(self):
        """
        Performs a full analysis of the source code.
        """
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                self.analysis[node.name] = self._analyze_function(node)
        return self.analysis

    def _analyze_function(self, func_node):
        """
        Analyzes a single function to determine its complexity characteristics.
        """
        recursion_type = self._check_recursion(func_node)

        # Enrich the analysis with DBPedia definitions
        enrichment = {}
        if recursion_type == "primitive":
            enrichment["dbpedia_uri"] = "http://dbpedia.org/resource/Primitive_recursive_function"
            enrichment["abstract"] = get_abstract("Primitive_recursive_function")
        elif recursion_type == "general":
            enrichment["dbpedia_uri"] = "http://dbpedia.org/resource/General_recursive_function"
            enrichment["abstract"] = get_abstract("General_recursive_function")

        return {
            "recursion_type": recursion_type,
            "enrichment": enrichment
        }

    def _check_recursion(self, func_node):
        """
        Checks a function for recursion and classifies it.
        """
        recursive_calls = []
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_node.name:
                    recursive_calls.append(node)

        if not recursive_calls:
            return "none"

        # For a function to be primitive recursive, all of its recursive calls
        # must be on structurally smaller arguments.
        for call in recursive_calls:
            if not self._is_primitive_recursive_call(call, func_node):
                return "general"

        return "primitive"

    def _is_primitive_recursive_call(self, call_node, func_node):
        """
        Checks if a specific recursive call site appears to be a valid
        primitive recursive call.

        A call is considered primitive recursive if:
        1. None of its arguments are nested recursive calls.
        2. At least one argument is structurally smaller (e.g., n - 1).
        """
        # 1. Check for nested recursive calls
        for arg in call_node.args:
            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == func_node.name:
                return False  # Found a nested call, so not primitive.

        # 2. Check for a structurally smaller argument
        is_smaller = False
        if not call_node.args or not func_node.args.args:
            return False

        for i, arg in enumerate(call_node.args):
            if i < len(func_node.args.args):
                original_arg_name = func_node.args.args[i].arg
                if (
                    isinstance(arg, ast.BinOp)
                    and isinstance(arg.op, ast.Sub)
                    and isinstance(arg.left, ast.Name)
                    and arg.left.id == original_arg_name
                    and isinstance(arg.right, ast.Constant)
                    and isinstance(arg.right.value, int)
                    and arg.right.value > 0
                ):
                    is_smaller = True
                    break

        return is_smaller
