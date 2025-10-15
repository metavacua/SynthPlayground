from enum import Enum
from collections import deque
from .proof import ProofTree
from . import translations

class Logic(Enum):
    LJ = "Intuitionistic Logic"
    LK = "Classical Logic"
    ILL = "Intuitionistic Linear Logic"
    LL = "Classical Linear Logic"

class Diagram:
    def __init__(self):
        self._graph = {
            Logic.LJ: {
                Logic.LK: translations.lj_to_lk,
                Logic.ILL: translations.lj_to_ill_proof,
            },
            Logic.ILL: {
                Logic.LL: translations.ill_to_ll,
            },
            Logic.LK: {},
            Logic.LL: {},
        }
        # Add reverse translations if they exist, or other sides of the diamond
        # For now, this represents the implemented translations.

    def find_path(self, start: Logic, end: Logic):
        """Finds a path of translations from a start logic to an end logic using BFS."""
        if start == end:
            return []

        queue = deque([(start, [])])
        visited = {start}

        while queue:
            current_logic, path = queue.popleft()

            for neighbor, translation_func in self._graph.get(current_logic, {}).items():
                if neighbor == end:
                    return path + [translation_func]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [translation_func]))

        return None # No path found

    def translate(self, proof: ProofTree, start: Logic, end: Logic) -> ProofTree:
        """Translates a proof from a starting logic to an ending logic."""
        path = self.find_path(start, end)
        if path is None:
            raise ValueError(f"No translation path found from {start.name} to {end.name}")

        translated_proof = proof
        for translation_func in path:
            translated_proof = translation_func(translated_proof)

        return translated_proof

# Example usage:
if __name__ == '__main__':
    from .formulas import Prop, Implies
    from . import lj

    # 1. Create a simple LJ proof
    A = Prop("A")
    lj_axiom_proof = lj.axiom(A)
    lj_proof = lj.implies_right(lj_axiom_proof, Implies(A, A))

    print("--- Original LJ Proof ---")
    print(lj_proof)

    # 2. Use the diagram to translate it
    diagram = Diagram()

    # Translate LJ -> LK
    try:
        lk_proof = diagram.translate(lj_proof, Logic.LJ, Logic.LK)
        print("\n--- Translated to LK ---")
        print(lk_proof)
    except ValueError as e:
        print(e)

    # Translate LJ -> LL (via ILL)
    try:
        # Note: This will use the placeholder lj_to_ill_proof translation
        ll_proof = diagram.translate(lj_proof, Logic.LJ, Logic.LL)
        print("\n--- Translated to LL (via ILL) ---")
        print(ll_proof)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(f"Translation to LL failed as expected due to placeholder: {e}")