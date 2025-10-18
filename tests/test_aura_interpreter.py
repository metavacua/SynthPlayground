import unittest
from aura_lang.lexer import Lexer
from aura_lang.parser import Parser
from aura_lang.interpreter import evaluate, Environment, BUILTINS

class TestAuraInterpreter(unittest.TestCase):

    def run_script(self, source):
        lexer = Lexer(source)
        parser = Parser(lexer)
        program = parser.parse_program()
        self.assertEqual(len(parser.errors), 0, f"Parser errors: {parser.errors}")
        env = Environment()
        for name, builtin in BUILTINS.items():
            env.set(name, builtin)
        result = evaluate(program, env)
        return result

    def test_integer_comparison_operators(self):
        # This script uses > and <, which are not implemented yet.
        # It should fail before the fix.
        script = """
        if (5 > 3) {
            return 1;
        } else {
            return 0;
        }
        """
        result = self.run_script(script)
        self.assertEqual(result.value, 1)

        script = """
        if (3 < 5) {
            return 1;
        } else {
            return 0;
        }
        """
        result = self.run_script(script)
        self.assertEqual(result.value, 1)

        script = """
        if (5 > 5) {
            return 1;
        } else {
            return 0;
        }
        """
        result = self.run_script(script)
        self.assertEqual(result.value, 0)

        script = """
        if (3 < 3) {
            return 1;
        } else {
            return 0;
        }
        """
        result = self.run_script(script)
        self.assertEqual(result.value, 0)

if __name__ == '__main__':
    unittest.main()