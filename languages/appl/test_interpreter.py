import unittest
from .ast import (
    Int,
    String,
    Bool,
    Unit,
    Var,
    Fun,
    App,
    Pair,
    LetPair,
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
from .interpreter import interpret, InterpError, Closure
from .planning import Action


class TestInterpreter(unittest.TestCase):
    def test_literals(self):
        self.assertEqual(interpret(Int(1)), Int(1))
        self.assertEqual(interpret(String("hello")), String("hello"))
        self.assertEqual(interpret(Bool(True)), Bool(True))
        self.assertEqual(interpret(Unit()), Unit())

    def test_var(self):
        env = {'x': Int(1)}
        self.assertEqual(interpret(Var('x'), env), Int(1))

    def test_var_not_found(self):
        with self.assertRaises(InterpError):
            interpret(Var('x'))

    def test_fun(self):
        # Test that a function evaluates to a closure
        id_fun = Fun('x', TInt(), Var('x'))
        self.assertIsInstance(interpret(id_fun), Closure)

    def test_app(self):
        # Test a simple function application
        id_fun = Fun('x', TInt(), Var('x'))
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
        let_pair = LetPair('x', 'y', Pair(Int(1), String("hello")), Var('x'))
        self.assertEqual(interpret(let_pair), Int(1))

    def test_inl_inr(self):
        self.assertEqual(interpret(Inl(Int(1), TString())), Inl(Int(1), TString()))
        self.assertEqual(interpret(Inr(String("hello"), TInt())), Inr(String("hello"), TInt()))

    def test_case(self):
        case_exp = Case(Inl(Int(1), TString()), 'x', Var('x'), 'y', Int(2))
        self.assertEqual(interpret(case_exp), Int(1))

    def test_promote(self):
        self.assertEqual(interpret(Promote(Int(1))), Int(1))

    def test_let_bang(self):
        let_bang = LetBang('x', Promote(Int(1)), Var('x'))
        self.assertEqual(interpret(let_bang), Int(1))

    def test_list(self):
        my_list = Cons(Int(1), Cons(Int(2), Nil(TInt())))
        self.assertEqual(interpret(my_list), my_list)

    def test_planning_primitive(self):
        # create_action("move", ["at A"], ["at B"])
        program = App(
            App(
                App(Var("create_action"), String("move")),
                Cons(String("at A"), Nil(TString()))
            ),
            Cons(String("at B"), Nil(TString()))
        )

        result = interpret(program)
        self.assertIsInstance(result, Action)
        self.assertEqual(result.name, "move")
        self.assertEqual(result.preconditions, ["at A"])
        self.assertEqual(result.effects, ["at B"])

    def test_homoiconicity(self):
        program = App(Var("eval"), App(Var("parse"), String('"hello"')))
        self.assertEqual(interpret(program), String("hello"))


if __name__ == '__main__':
    unittest.main()
