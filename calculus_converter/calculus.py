import json

class Sequent:
    """Represents a logical sequent of the form 'antecedent ⊢ succedent'."""
    def __init__(self, raw_sequent):
        self.raw = raw_sequent.strip()
        parts = self.raw.split('⊢')
        self.antecedent = parts[0].strip() if len(parts) > 1 else ""
        self.succedent = parts[1].strip() if len(parts) > 1 else parts[0].strip()

    def __repr__(self):
        return f"Sequent({self.antecedent} ⊢ {self.succedent})"

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
        if not proof_tree_data:
            return
        tree = self._build_tree_recursively(proof_tree_data)
        if tree:
            self.add_element("prooftree", tree)

    def _build_tree_recursively(self, tree_data):
        if not tree_data:
            return None

        hyp_objects = []
        for h_data in tree_data.get('hypotheses', []):
            if not h_data: continue # Skip any None entries

            if h_data.get('type') == 'hypo':
                hyp_objects.append(Sequent(h_data['content']))
            elif h_data.get('type') == 'prooftree': # It's a nested prooftree dict
                nested_tree = self._build_tree_recursively(h_data)
                if nested_tree:
                    hyp_objects.append(nested_tree)

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
                hyp_list.append({"type": "sequent", "content": h.raw})
            elif isinstance(h, ProofTree):
                hyp_list.append(self._prooftree_to_dict(h)) # Recurse

        return {
            "type": "prooftree",
            "rule": tree.rule_name,
            "conclusion": tree.conclusion.raw,
            "hypotheses": hyp_list
        }