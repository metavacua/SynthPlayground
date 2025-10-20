"""
A compiler that translates AURA code to LFI-ILL.

This script takes an AURA file, parses it, and compiles it into an LFI-ILL
AST. The resulting AST is then written to a `.lfi_ill` file.
"""

import argparse
import sys
import os

# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aura_lang.lexer import Lexer as AuraLexer
from aura_lang.parser import Parser as AuraParser
from aura_lang.ast import (
    LetStatement,
    IntegerLiteral,
    StringLiteral,
    InfixExpression,
    Identifier,
    CallExpression,
    PrintStatement,
    IfStatement,
    ForStatement,
    ReturnStatement,
    FunctionDefinition,
    BlockStatement,
    ExpressionStatement,
)
from lfi_ill import (
    LetTensor,
    Int,
    Var,
    Fun,
    App,
    TensorPair,
    Promotion,
    Dereliction,
    LetWhyNot,
    WhyNot,
    Par,
    LetPar,
    Unit,
    Case,
    String,
)


class AuraToLfiIllCompiler:
    def __init__(self):
        pass

    def compile(self, node):
        method_name = f"compile_{type(node).__name__}"
        compiler = getattr(self, method_name, self.generic_compiler)
        return compiler(node)

    def generic_compiler(self, node):
        raise Exception(f"No compile_{type(node).__name__} method")

    def compile_Program(self, node):
        # This is a simplification. A more robust implementation would
        # handle the sequence of statements in the program.
        if node.statements:
            return self.compile(node.statements[0])
        return Unit()

    def compile_LetStatement(self, node):
        var = Var(node.name.value)
        val = self.compile(node.value)
        # The body of the let statement is not yet handled.
        # We'll represent it as a placeholder.
        body_placeholder = Unit()
        return Dereliction(var, Promotion(val), body_placeholder)

    def compile_ExpressionStatement(self, node):
        return self.compile(node.expression)

    def compile_IntegerLiteral(self, node):
        return Int(node.value)

    def compile_StringLiteral(self, node):
        return String(node.value)

    def compile_Identifier(self, node):
        return Var(node.value)

    def compile_InfixExpression(self, node):
        left = self.compile(node.left)
        right = self.compile(node.right)
        return TensorPair(left, right)  # Simplification

    def compile_CallExpression(self, node):
        function = self.compile(node.function)
        args = [self.compile(arg) for arg in node.arguments]
        if args:
            return App(function, args[0])  # Simplification
        else:
            return App(function, Unit())

    def compile_PrintStatement(self, node):
        arg = self.compile(node.value)
        return App(Var("print"), arg)

    def compile_IfStatement(self, node):
        cond = self.compile(node.condition)
        cons = self.compile(node.consequence)
        alt = self.compile(node.alternative) if node.alternative else Unit()
        return Case(cond, Var("true"), cons, Var("false"), alt)

    def compile_BlockStatement(self, node):
        # This is a simplification. A more robust implementation would
        # handle the sequence of statements in the block.
        if node.statements:
            return self.compile(node.statements[0])
        return Unit()

    def compile_ForStatement(self, node):
        iterable = self.compile(node.iterable)
        body = self.compile(node.body)
        return App(Var("for"), TensorPair(iterable, body))

    def compile_ReturnStatement(self, node):
        return self.compile(node.value)

    def compile_FunctionDefinition(self, node):
        name = self.compile(node.name)
        body = self.compile(node.body)
        return Fun(name, TFun(TUnit(), TUnit()), body)


def main():
    parser = argparse.ArgumentParser(description="Compile AURA code to LFI ILL.")
    parser.add_argument("file", help="The AURA file to compile.")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as f:
            aura_code = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}")
        return

    lexer = AuraLexer(aura_code)
    parser = AuraParser(lexer)
    aura_program = parser.parse_program()

    if parser.errors:
        print("AURA parsing errors:")
        for error in parser.errors:
            print(error)
        return

    compiler = AuraToLfiIllCompiler()
    lfi_ill_ast = compiler.compile(aura_program)

    print("--- COMPILED LFI ILL AST ---")
    print(repr(lfi_ill_ast))

    output_filename = args.file.replace(".aura", ".lfi_ill")
    with open(output_filename, "w") as f:
        f.write(repr(lfi_ill_ast))

    print(f"\nSuccessfully compiled to {output_filename}")


if __name__ == "__main__":
    main()
