"""
This module defines the CRE_Orchestrator, the high-level interface for the
Categorical Reasoning Engine's cognitive cycle.
"""

import os
import sys
import json

# Add the repository root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tooling.witness_registry import WitnessRegistry
from tooling.refactoring_registry import RefactoringRegistry
from tooling.problem_classifier import classify_file
from tooling.refactoring_engine import RefactoringEngine
from tooling.proof_synthesizer import ProofSynthesizer
from logic_system.functor import CorrespondenceFunctor

class CRE_Orchestrator:
    """
    Encapsulates the full cognitive cycle of the CRE, providing a high-level
    API for meta-logical propositions.
    """

    def __init__(self):
        self.witness_registry = WitnessRegistry()
        self.refactoring_registry = RefactoringRegistry()
        self.functor = CorrespondenceFunctor()

        # Initialize registries
        self.witness_registry.scan()
        self.refactoring_registry.scan()

        self.refactoring_engine = RefactoringEngine(self.refactoring_registry)
        self.proof_synthesizer = ProofSynthesizer(self.functor)

    def prove_termination(self, source_file: str) -> (str, dict):
        """
        A meta-logical proposition. Given a source file, this method attempts to
        produce a new artifact that is provably terminating.

        Returns:
            A tuple containing the path to the refactored file and the formal proof of termination.
        """
        print(f"--- CRE: Received proposition 'prove_termination' for {source_file} ---")

        # 1. Classify the input artifact
        classification = classify_file(source_file, self.witness_registry)
        source_class = classification['name']
        print(f"Step 1: Classified '{source_file}' as '{source_class}'")

        if source_class == "Recursive Languages":
            print("Artifact is already in a decidable class. Proceeding directly to proof.")
            refactored_file = source_file
        else:
            # 2. Find a refactoring path to a decidable class
            target_class = "Recursive Languages"
            print(f"Step 2: Identifying morphism from '{source_class}' to '{target_class}'")

            # 3. Execute the transformation
            refactored_file = self.refactoring_engine.find_and_execute(source_file, source_class, target_class)
            print(f"Step 3: Executed refactoring. New artifact at '{refactored_file}'")

        # 4. Synthesize the proof for the new artifact
        print(f"Step 4: Synthesizing termination proof for '{refactored_file}'")
        proof = self.proof_synthesizer.synthesize(refactored_file, "Recursive Languages", "termination")

        print("--- CRE: Proposition successfully resolved. ---")
        return (refactored_file, proof)

if __name__ == '__main__':
    # --- Demonstration of the full cognitive cycle ---
    orchestrator = CRE_Orchestrator()

    # Define the problem artifact
    unbounded_file = "poc/unbounded_loop.py"

    # Execute the meta-proposition
    final_artifact, termination_proof = orchestrator.prove_termination(unbounded_file)

    print("\n--- Final Result ---")
    print(f"Final Artifact: {final_artifact}")
    print("Termination Proof:")
    print(json.dumps(termination_proof, indent=2))
    print("--------------------")
