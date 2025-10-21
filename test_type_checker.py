import unittest
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
    Inl,
    Inr,
    Case,
    Promote,
    LetBang,
    TInt,
    TString,
    TBool,
    TUnit,
    TFun,
    TExponential,
    TProd,
    TSum,
)
from type_checker import type_check, TypeCheckError


class TestTypeChecker(unittest.TestCase):
    def test_literals(self):
        self.assertEqual(type_check(Int(1)), TInt())
        self.assertEqual(type_check(String("hello")), TString())
        self.assertEqual(type_check(Bool(True)), TBool())
        self.assertEqual(type_check(Unit()), TUnit())

    def test_var_unrestricted(self):
        context = {"x": TInt()}
        self.assertEqual(type_check(Var("x"), unrestricted_context=context), TInt())

    def test_var_linear(self):
        context = {"x": TInt()}
        self.assertEqual(type_check(Var("x"), linear_context=context), TInt())

    def test_var_not_found(self):
        with self.assertRaises(TypeCheckError):
            type_check(Var("x"))

    def test_fun(self):
        # Test a simple identity function
        id_fun = Fun("x", TInt(), Var("x"))
        self.assertEqual(type_check(id_fun), TFun(TInt(), TInt()))

    def test_fun_unrestricted(self):
        # Test a function with an unrestricted argument
        id_fun = Fun("x", TExponential(TInt()), Var("x"))
        self.assertEqual(type_check(id_fun), TFun(TExponential(TInt()), TInt()))

    def test_app(self):
        # Test a simple function application
        id_fun = Fun("x", TInt(), Var("x"))
        app = App(id_fun, Int(1))
        self.assertEqual(type_check(app), TInt())

    def test_app_type_mismatch(self):
        # Test a function application with a type mismatch
        id_fun = Fun("x", TInt(), Var("x"))
        app = App(id_fun, String("hello"))
        with self.assertRaises(TypeCheckError):
            type_check(app)

    def test_pair(self):
        pair = Pair(Int(1), String("hello"))
        self.assertEqual(type_check(pair), TProd(TInt(), TString()))

    def test_let_pair(self):
        # Consume both variables to satisfy the linear type checker.
        let_pair = LetPair(
            "x", "y", Pair(Int(1), String("hello")), Pair(Var("x"), Var("y"))
        )
        self.assertEqual(type_check(let_pair), TProd(TInt(), TString()))

    def test_inl_inr(self):
        self.assertEqual(type_check(Inl(Int(1), TString())), TSum(TInt(), TString()))
        self.assertEqual(
            type_check(Inr(String("hello"), TInt())), TSum(TInt(), TString())
        )

    def test_case(self):
        case_exp = Case(Inl(Int(1), TInt()), "x", Var("x"), "y", Var("y"))
        self.assertEqual(type_check(case_exp), TInt())

    def test_case_type_mismatch(self):
        case_exp = Case(Inl(Int(1), TString()), "x", Var("x"), "y", Var("y"))
        with self.assertRaisesRegex(TypeCheckError, "Type mismatch in case branches"):
            type_check(case_exp)

    def test_promote(self):
        self.assertEqual(type_check(Promote(Int(1))), TExponential(TInt()))

    def test_promote_linear_error(self):
        with self.assertRaises(TypeCheckError):
            type_check(Promote(Var("x")), linear_context={"x": TInt()})

    def test_let_bang(self):
        let_bang = LetBang("x", Promote(Int(1)), Var("x"))
        self.assertEqual(type_check(let_bang), TInt())

    def test_unused_linear_variable(self):
        with self.assertRaises(TypeCheckError):
            type_check(Int(1), linear_context={"x": TInt()})


if __name__ == "__main__":
    unittest.main()
