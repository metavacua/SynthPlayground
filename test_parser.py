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
    Cons,
    Nil,
    TInt,
    TString,
)
from parser import parse


class TestParser(unittest.TestCase):

    def test_literals(self):
        self.assertEqual(parse("1"), Int(1))
        self.assertEqual(parse("true"), Bool(True))
        self.assertEqual(parse('"hello"'), String("hello"))

    def test_var(self):
        self.assertEqual(parse("x"), Var("x"))

    def test_fun(self):
        self.assertEqual(parse("fn x : Int => x"), Fun("x", TInt(), Var("x")))

    def test_app(self):
        self.assertEqual(parse("f x"), App(Var("f"), Var("x")))
        self.assertEqual(parse("f x y"), App(App(Var("f"), Var("x")), Var("y")))
        self.assertEqual(parse("f (g x)"), App(Var("f"), App(Var("g"), Var("x"))))

    def test_pair(self):
        self.assertEqual(parse("(1, 2)"), Pair(Int(1), Int(2)))

    def test_let_pair(self):
        self.assertEqual(
            parse("let (x, y) = (1, 2) in x"),
            LetPair("x", "y", Pair(Int(1), Int(2)), Var("x")),
        )

    def test_inl_inr(self):
        self.assertEqual(parse("inl(1, String)"), Inl(Int(1), TString()))
        self.assertEqual(parse("inr(true, Int)"), Inr(Bool(True), TInt()))

    def test_case(self):
        self.assertEqual(
            parse("case inl(1, String) of inl x => x | inr y => 2"),
            Case(Inl(Int(1), TString()), "x", Var("x"), "y", Int(2)),
        )

    def test_promote(self):
        self.assertEqual(parse("!x"), Promote(Var("x")))

    def test_let_bang(self):
        self.assertEqual(
            parse("let !x = !y in x"), LetBang("x", Promote(Var("y")), Var("x"))
        )

    def test_complex_expression(self):
        code = """
        let (f, g) = (fn x : Int => x, fn y : Int => y) in
        case inl(f 1, Int) of
            inl x => x
          | inr y => g 2
        """
        expected = LetPair(
            "f",
            "g",
            Pair(Fun("x", TInt(), Var("x")), Fun("y", TInt(), Var("y"))),
            Case(
                Inl(App(Var("f"), Int(1)), TInt()),
                "x",
                Var("x"),
                "y",
                App(Var("g"), Int(2)),
            ),
        )
        # A bit of a hack, because parse() has a side effect of tokenizing the code
        # We need to make sure the code is parsed correctly
        self.assertEqual(parse(code), expected)

    def test_parse_error(self):
        with self.assertRaisesRegex(
            ValueError,
            r"Expected 'in' but got 'let' at position 12. Remaining tokens: \['let', 'z', '=', 'x', 'in', 'z'\]",
        ):
            parse("let (x, y) = (1, 2) let z = x in z")

    def test_unit(self):
        self.assertEqual(parse("unit"), Unit())

    def test_nil(self):
        self.assertEqual(parse("Nil(Int)"), Nil(TInt()))

    def test_cons(self):
        self.assertEqual(
            parse("1 :: 2 :: Nil(Int)"), Cons(Int(1), Cons(Int(2), Nil(TInt())))
        )


if __name__ == "__main__":
    unittest.main()
