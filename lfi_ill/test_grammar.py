import unittest
from lfi_ill.lexer import lexer
from lfi_ill.parser import parser
from lfi_ill.ast import *

class TestGrammar(unittest.TestCase):
    def test_tensor_parsing(self):
        data = 'p ⊗ q'
        result = parser.parse(data, lexer=lexer)
        expected = Tensor(Atom('p'), Atom('q'))
        self.assertEqual(repr(result), repr(expected))

    def test_par_parsing(self):
        data = 'p ⅋ q'
        result = parser.parse(data, lexer=lexer)
        expected = Par(Atom('p'), Atom('q'))
        self.assertEqual(repr(result), repr(expected))

    def test_negation_parsing(self):
        data = '¬p'
        result = parser.parse(data, lexer=lexer)
        expected = Negation(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

    def test_consistency_parsing(self):
        data = '∘p'
        result = parser.parse(data, lexer=lexer)
        expected = Consistency(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

    def test_of_course_parsing(self):
        data = '!p'
        result = parser.parse(data, lexer=lexer)
        expected = OfCourse(Atom('p'))
        self.assertEqual(repr(result), repr(expected))

if __name__ == '__main__':
    unittest.main()