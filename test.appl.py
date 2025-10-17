from appl_ast import *

# A simple APPL program: let !x = !5 in x * x
# This will be translated to LFI ILL.
# The compiler expects the AST to be assigned to a variable named APPL_AST.
APPL_AST = AST(
    LetBang(
        Var('x'),
        Promote(Int(5)),
        Pair(
            Var('x'),
            Var('x')
        )
    )
)