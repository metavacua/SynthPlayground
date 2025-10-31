# tests/aura/test_aura_parser.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import unittest
from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.ast import (
    Program, LetStatement, Identifier, FunctionDefinition, TypedIdentifier
)

class TestAuraParser(unittest.TestCase):
    def test_let_statement(self):
        source_code = "let x = 5;"
        l = Lexer(source_code)
        p = Parser(l)
        program = p.parse_program()
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, LetStatement)
        self.assertEqual(stmt.name.value, "x")

    def test_function_definition(self):
        source_code = "func my_func(a: int, b: str) -> bool { let x = 5; }"
        l = Lexer(source_code)
        p = Parser(l)
        program = p.parse_program()
        self.assertEqual(len(program.statements), 1)
        stmt = program.statements[0]
        self.assertIsInstance(stmt, FunctionDefinition)
        self.assertEqual(stmt.name.value, "my_func")
        self.assertEqual(len(stmt.params), 2)
        self.assertIsInstance(stmt.params[0], TypedIdentifier)
        self.assertEqual(stmt.params[0].value, "a")
        self.assertEqual(stmt.params[0].type_name, "int")
        self.assertIsInstance(stmt.params[1], TypedIdentifier)
        self.assertEqual(stmt.params[1].value, "b")
        self.assertEqual(stmt.params[1].type_name, "str")
        self.assertEqual(stmt.return_type.value, "bool")

if __name__ == "__main__":
    unittest.main()
