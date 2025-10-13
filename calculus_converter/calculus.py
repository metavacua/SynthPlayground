import json
import re

class Formula:
    """Represents a parsed logical formula with its structure."""
    def __init__(self, content):
        self.raw = content.strip()
        # This is a simple recursive descent parser for the formulas.
        self.structure = self._parse_formula(self.raw)

    def _parse_formula(self, text):
        text = text.strip()

        # This is a very basic parser that doesn't handle precedence or associativity correctly.
        # It's a demonstration of creating a structured representation.
        # It splits on the first found operator.

        # Binary operators
        for op in ['→', '⊕', '⊗', '&', '℘']:
            # Be careful not to split inside parentheses (not handled here)
            if op in text:
                parts = text.split(op, 1)
                if len(parts) == 2 and parts[0].strip() and parts[1].strip():
                    return {
                        "type": "binary",
                        "op": op,
                        "left": self._parse_formula(parts[0]),
                        "right": self._parse_formula(parts[1])
                    }

        # Unary operator
        if text.startswith('¬'):
            return {
                "type": "unary",
                "op": '¬',
                "operand": self._parse_formula(text[1:])
            }

        # Atomic formula (variable or constant)
        return {"type": "atom", "name": text}

    def to_dict(self):
        return self.structure

    def __repr__(self):
        return f"Formula({self.raw})"

class Sequent:
    """Represents a logical sequent with structured formulas."""
    def __init__(self, raw_sequent):
        self.raw = raw_sequent.strip()
        parts = self.raw.split('⊢')

        antecedent_str = parts[0].strip() if len(parts) > 1 else ""
        succedent_str = parts[1].strip() if len(parts) > 1 else parts[0].strip()

        # Formulas in antecedent/succedent are separated by commas
        self.antecedent = [Formula(f) for f in antecedent_str.split(',') if f.strip()] if antecedent_str else []
        self.succedent = [Formula(f) for f in succedent_str.split(',') if f.strip()] if succedent_str else []

    def to_dict(self):
        return {
            "antecedent": [f.to_dict() for f in self.antecedent],
            "succedent": [f.to_dict() for f in self.succedent]
        }

    def __repr__(self):
        ant_str = ", ".join(f.raw for f in self.antecedent)
        suc_str = ", ".join(f.raw for f in self.succedent)
        return f"Sequent({ant_str} ⊢ {suc_str})"

class ProofTree:
    """Represents a potentially nested proof tree."""
    def __init__(self, conclusion, rule_name, hypotheses=None):
        self.hypotheses = hypotheses if hypotheses else [] # List of Sequent or ProofTree
        self.conclusion = Sequent(conclusion)
        self.rule_name = rule_name

    def __repr__(self):
        return f"ProofTree(Rule: {self.rule_name}, Conclusion: {self.conclusion})"

class Document:
    """Represents the entire content of a parsed LaTeX file."""
    def __init__(self):
        self.title = "Untitled"
        self.author = None
        self.elements = []

    def add_element(self, element_type, content):
        self.elements.append((element_type, content))

    def add_proof_tree(self, proof_tree_data):
        tree = self._build_tree_recursively(proof_tree_data)
        self.add_element("prooftree", tree)

    def _build_tree_recursively(self, tree_data):
        hyp_objects = []
        for h_data in tree_data.get('hypotheses', []):
            if h_data.get('type') == 'hypo':
                hyp_objects.append(Sequent(h_data['content']))
            elif h_data.get('type') == 'prooftree': # It's a nested prooftree dict
                hyp_objects.append(self._build_tree_recursively(h_data))

        return ProofTree(
            hypotheses=hyp_objects,
            conclusion=tree_data['conclusion'],
            rule_name=tree_data['rule_name']
        )

    def to_json(self):
        """Serializes the document to a JSON-friendly format for inspection."""
        doc_repr = {
            "title": self.title,
            "author": self.author,
            "elements": []
        }
        for type, element in self.elements:
            if type == "prooftree":
                doc_repr["elements"].append(self._prooftree_to_dict(element))
            else:
                doc_repr["elements"].append({"type": type, "content": element})
        return json.dumps(doc_repr, indent=2)

    def _prooftree_to_dict(self, tree):
        hyp_list = []
        for h in tree.hypotheses:
            if isinstance(h, Sequent):
                hyp_list.append({"type": "sequent", "raw": h.raw, **h.to_dict()})
            elif isinstance(h, ProofTree):
                # ProofTree objects don't have a to_dict, so we recurse
                hyp_list.append(self._prooftree_to_dict(h))

        return {
            "type": "prooftree",
            "rule": tree.rule_name,
            "conclusion": {
                "raw": tree.conclusion.raw,
                **tree.conclusion.to_dict()
            },
            "hypotheses": hyp_list,
        }