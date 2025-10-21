import unittest
import os
from appl_ast import (
    Int,
    String,
    Bool,
    Unit,
    Var,
    Fun,
    App,
    Pair,
    LetPair,
    Let,
    Inl,
    Inr,
    Case,
    Promote,
    LetBang,
    Cons,
    Nil,
    TInt,
    TString,
)
from interpreter import interpret, InterpError, Closure


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        """Create a dummy AAL file for testing."""
        self.aal_filepath = "tests/test.aal"
        with open(self.aal_filepath, "w") as f:
            f.write("fluent at_A\n")
            f.write("fluent at_B\n")
            f.write("action move\n")
            f.write("move causes at_B if at_A\n")

    def tearDown(self):
        """Clean up the dummy AAL file."""
        if os.path.exists(self.aal_filepath):
            os.remove(self.aal_filepath)

    def test_literals(self):
        self.assertEqual(interpret(Int(1)), Int(1))
        self.assertEqual(interpret(String("hello")), String("hello"))
        self.assertEqual(interpret(Bool(True)), Bool(True))
        self.assertEqual(interpret(Unit()), Unit())

    def test_var(self):
        env = {"x": Int(1)}
        self.assertEqual(interpret(Var("x"), env), Int(1))

    def test_var_not_found(self):
        with self.assertRaises(InterpError):
            interpret(Var("x"))

    def test_fun(self):
        # Test that a function evaluates to a closure
        id_fun = Fun("x", TInt(), Var("x"))
        self.assertIsInstance(interpret(id_fun), Closure)

    def test_app(self):
        # Test a simple function application
        id_fun = Fun("x", TInt(), Var("x"))
        app = App(id_fun, Int(1))
        self.assertEqual(interpret(app), Int(1))

    def test_app_non_function(self):
        # Test applying a non-function
        app = App(Int(1), Int(2))
        with self.assertRaises(InterpError):
            interpret(app)

    def test_pair(self):
        pair = Pair(Int(1), String("hello"))
        self.assertEqual(interpret(pair), Pair(Int(1), String("hello")))

    def test_let_pair(self):
        let_pair = LetPair("x", "y", Pair(Int(1), String("hello")), Var("x"))
        self.assertEqual(interpret(let_pair), Int(1))

    def test_inl_inr(self):
        self.assertEqual(interpret(Inl(Int(1), TString())), Inl(Int(1), TString()))
        self.assertEqual(
            interpret(Inr(String("hello"), TInt())), Inr(String("hello"), TInt())
        )

    def test_case(self):
        case_exp = Case(Inl(Int(1), TString()), "x", Var("x"), "y", Int(2))
        self.assertEqual(interpret(case_exp), Int(1))

    def test_promote(self):
        self.assertEqual(interpret(Promote(Int(1))), Int(1))

    def test_let_bang(self):
        let_bang = LetBang("x", Promote(Int(1)), Var("x"))
        self.assertEqual(interpret(let_bang), Int(1))

    def test_list(self):
        my_list = Cons(Int(1), Cons(Int(2), Nil(TInt())))
        self.assertEqual(interpret(my_list), my_list)

    def test_aal_integration(self):
        # This test now verifies the AAL integration.
        program = Let(
            "!domain",
            App(Var("load_domain"), String(self.aal_filepath)),
            Let(
                "!state1",
                App(Var("create_state"), Cons(String("at_A"), Nil(TString()))),
                Let(
                    "!state2",
                    App(Var("apply_action"), String("move")),
                    App(Var("is_goal"), Cons(String("at_B"), Nil(TString()))),
                ),
            ),
        )
        result = interpret(program)
        self.assertEqual(result, Bool(True))

    def test_homoiconicity(self):
        program = App(Var("eval"), App(Var("parse"), String('"hello"')))
        self.assertEqual(interpret(program), String("hello"))


if __name__ == "__main__":
    unittest.main()
