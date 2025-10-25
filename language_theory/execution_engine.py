import yaml
import json
import re
import sys
import os

# Ensure the root directory is in the path to allow importing dbpedia_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from identify_methodology import analyze_repository
from dbpedia_client import search_resources, get_abstract

class TaskExecutionEngine:
    def __init__(self, protocols_path='language_theory/protocols.yaml', repo_path='.'):
        """
        Initializes the engine with protocols and repository analysis.
        """
        self.protocols = self._load_protocols(protocols_path)
        self.repo_context = analyze_repository(repo_path)
        print("--- Repository Context Analysis ---")
        print(json.dumps(self.repo_context, indent=2))
        print("------------------------------------")

    def _load_protocols(self, path):
        """Loads the operating protocols from the YAML file."""
        with open(path, 'r') as f:
            return yaml.safe_load(f)

    def _enrich_with_domain_context(self, task_description):
        """
        Uses the dbpedia_client to fetch context for keywords in the task description.
        """
        # A simple heuristic to extract potential keywords (nouns and capitalized words)
        keywords = [word for word in re.findall(r'\b[A-Z][a-z]*\w+\b', task_description)]

        # Filter out common programming verbs that might be capitalized at the start of a sentence
        common_verbs = ["Implement", "Modify", "Create", "Add", "Update", "Remove", "Delete", "Fix"]
        filtered_keywords = [kw for kw in keywords if kw not in common_verbs]

        if not filtered_keywords:
            print(f"\n[No suitable domain keywords found in task description]")
            return None

        print(f"\n[Enriching Domain Context for keywords: {filtered_keywords}]")

        # For this PoC, we'll just use the first keyword found
        keyword = filtered_keywords[0]
        resources = search_resources(keyword)

        if not resources:
            print(f"- No DBpedia resources found for '{keyword}'.")
            return None

        # Get the abstract for the first resource found
        resource_name = resources[0]
        abstract = get_abstract(resource_name)

        if abstract:
            print(f"- Context for '{resource_name}': {abstract[:200]}...") # Print a snippet
            return abstract
        return None

    def get_applicable_protocols(self, task_description):
        """
        Determines which protocols are applicable based on the repository context
        and task description.
        """
        applicable = {
            'core': self.protocols['core_philosophy']['principles'],
            'methodology_specific': [],
            'risk_mitigation': [],
            'warnings': []
        }

        # Check for TDD/XP
        if 'test_driven_development_xp' in self.repo_context:
            if "add feature" in task_description.lower() or "implement" in task_description.lower():
                rule = self.protocols['methodology_protocols']['test_driven_development']['frictions_and_mitigations'][0]
                applicable['methodology_specific'].append(f"TDD/XP Detected: {rule}")

        # Check for DDD
        if 'domain_driven_design' in self.repo_context:
            core_paths = [
                item['path'] for item in self.repo_context['domain_driven_design']
                if item['type'] == 'Bounded Context Detected'
            ]
            if any(path in task_description for path in core_paths):
                 rule = self.protocols['methodology_protocols']['domain_driven_design']['frictions_and_mitigations'][0]
                 applicable['warnings'].append(f"DDD CORE DOMAIN: {rule}")


        # General risk mitigation for any code modification task
        if "code" in task_description.lower() or "feature" in task_description.lower() or "refactor" in task_description.lower():
            applicable['risk_mitigation'].extend(self.protocols['risk_mitigation_framework']['code_quality'])
            applicable['risk_mitigation'].extend(self.protocols['risk_mitigation_framework']['security'])


        return applicable

    def execute_task(self, task_description):
        """
        Simulates the execution of a task, applying the relevant protocols.
        """
        print(f"\n>>> Executing Task: '{task_description}'")

        # Step 1: Enrich context from DBpedia
        self._enrich_with_domain_context(task_description)

        # Step 2: Determine and apply protocols
        protocols_to_apply = self.get_applicable_protocols(task_description)

        print("\n[Applying Core Philosophy]")
        for principle in protocols_to_apply['core']:
            print(f"- {principle}")

        if protocols_to_apply['warnings']:
            print("\n[CRITICAL WARNINGS]")
            for warning in protocols_to_apply['warnings']:
                print(f"- {warning}")
                print("  ACTION: Halting autonomous execution. Requesting human review.")
            return

        if protocols_to_apply['methodology_specific']:
            print("\n[Applying Methodology-Specific Protocols]")
            for protocol in protocols_to_apply['methodology_specific']:
                print(f"- {protocol}")

        if protocols_to_apply['risk_mitigation']:
            print("\n[Applying Risk Mitigation Framework]")
            for rule in protocols_to_apply['risk_mitigation']:
                print(f"- {rule}")

        print("\n[Simulating Action Plan]")
        print("1. Generate a 'first draft' of the code.")
        print("2. Generate corresponding unit tests.")
        print("3. Run static analysis and security scans.")
        print("4. Submit for mandatory human review.")
        print("--- Task Simulation Complete ---")


if __name__ == "__main__":
    engine = TaskExecutionEngine()

    # --- Simulation 1: A standard feature with a searchable term ---
    engine.execute_task("Implement a new Caching feature for the data access layer.")

    # --- Simulation 2: A task that could touch a core DDD domain (hypothetical) ---
    engine.repo_context['domain_driven_design'] = [
        {'type': 'Bounded Context Detected', 'context_name': 'billing', 'path': './billing/'}
    ]
    print("\n\n--- Injecting DDD context for simulation ---")
    engine.execute_task("Modify the core Billing logic in './billing/domain/service.py'")
