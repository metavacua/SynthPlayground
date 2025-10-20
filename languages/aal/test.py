import unittest
from . import parser
from . import interpreter

class TestAAL(unittest.TestCase):

    def test_parse_and_interpret(self):
        """
        Tests that the AAL parser and interpreter can successfully parse and interpret an AAL file.
        """
        aal_data = parser.parse("languages/aal/logging-verification.aal")
        self.assertTrue(interpreter.interpret(aal_data))

if __name__ == '__main__':
    unittest.main()
