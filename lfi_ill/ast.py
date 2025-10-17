# AST Node classes
class Formula:
    pass

class Atom(Formula):
    def __init__(self, name, negated=False):
        self.name = name
        self.negated = negated
    def __repr__(self):
        return f"Atom({self.name}{'`' if self.negated else ''})"

class Tensor(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Tensor({self.left}, {self.right})"

class Par(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Par({self.left}, {self.right})"

class Plus(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"Plus({self.left}, {self.right})"

class With(Formula):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"With({self.left}, {self.right})"

class OfCourse(Formula):
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"OfCourse({self.formula})"

class WhyNot(Formula):
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"WhyNot({self.formula})"

class Section(Formula):
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"Section({self.formula})"

class Negation(Formula):
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"Negation({self.formula})"

class Consistency(Formula):
    def __init__(self, formula):
        self.formula = formula
    def __repr__(self):
        return f"Consistency({self.formula})"

class One(Formula):
    def __repr__(self):
        return "One"

class Bottom(Formula):
    def __repr__(self):
        return "Bottom"

class Zero(Formula):
    def __repr__(self):
        return "Zero"

class Top(Formula):
    def __repr__(self):
        return "Top"