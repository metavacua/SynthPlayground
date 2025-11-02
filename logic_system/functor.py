"""
This module defines the Correspondence Functor, F: CatFormLang -> CatLog.
It provides a formal, programmable mapping from language classes to their
corresponding logical systems.
"""

from typing import Dict

# This mapping defines the core of the functor. It maps the 'name' from a
# witness.json file to a specific logical system available in the logic_system package.
# For now, we are mapping to simplified, conceptual names. A future implementation
# would map to specific prover classes or configurations.
FUNCTOR_MAPPING: Dict[str, str] = {
    "Regular Languages": "Finite State Logic",
    "Context-Free Languages": "Pushdown Logic",
    "Context-Sensitive Languages": "Bounded Linear Logic",
    "Recursive Languages": "Constructive Logic (Intuitionistic)",
    "Recursively Enumerable Languages": "Classical Logic (Peano Arithmetic)"
}

class CorrespondenceFunctor:
    """
    Implements the functor F that maps objects from CatFormLang to CatLog.
    """

    def __init__(self, mapping: Dict[str, str] = FUNCTOR_MAPPING):
        self.mapping = mapping

    def apply(self, language_class_name: str) -> str:
        """
        Applies the functor to a language class to get the corresponding logic.

        Args:
            language_class_name: The 'name' of the language class object from CatFormLang.

        Returns:
            The name of the corresponding logical system in CatLog.
        """
        logic_system = self.mapping.get(language_class_name)
        if not logic_system:
            raise ValueError(f"No logical system mapping found for language class: {language_class_name}")
        return logic_system

if __name__ == '__main__':
    functor = CorrespondenceFunctor()

    # --- Demonstration ---
    print("--- Applying the Correspondence Functor ---")

    lang_class = "Recursive Languages"
    logic = functor.apply(lang_class)
    print(f"F({lang_class}) = {logic}")

    lang_class = "Recursively Enumerable Languages"
    logic = functor.apply(lang_class)
    print(f"F({lang_class}) = {logic}")

    print("-----------------------------------------")
