import unittest
import os
import json
from unittest.mock import patch, MagicMock

# Add the language_theory directory to the Python path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language_theory')))
# Add the root directory to the path to find dbpedia_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from identify_methodology import identify_ddd, identify_tdd_xp, identify_devops
from execution_engine import TaskExecutionEngine

class TestMethodologyIdentification(unittest.TestCase):

    def test_identify_ddd_with_bounded_contexts(self):
        """Should detect a Bounded Context with domain and application layers."""
        files = [
            './project/ordering/domain/',
            './project/ordering/application/',
            './project/ordering/infrastructure/',
            './project/ordering/domain/order.py',
            './project/ordering/application/order_service.py',
            './project/ordering/infrastructure/db_repo.py',
        ]
        evidence = identify_ddd(files)
        bc_evidence = next((item for item in evidence if item.get('type') == 'Bounded Context Detected'), None)
        self.assertIsNotNone(bc_evidence)
        self.assertEqual(bc_evidence['context_name'], 'ordering')
        self.assertEqual(bc_evidence['path'], './project/ordering')
        self.assertEqual(set(bc_evidence['found_layers']), {'domain', 'application', 'infrastructure'})

    def test_identify_ddd_with_ubiquitous_language_doc(self):
        files = ['./docs/ubiquitous-language.md']
        evidence = identify_ddd(files)
        self.assertIn({'type': 'Ubiquitous Language Document', 'file': './docs/ubiquitous-language.md'}, evidence)

    def test_identify_tdd_with_high_test_ratio(self):
        files = ['./src/main.py', './src/utils.py', './tests/test_main.py', './tests/test_utils.py']
        evidence = identify_tdd_xp(files)
        self.assertIn({'type': 'Conclusion', 'finding': 'High test-to-source ratio suggests a TDD/XP culture.'}, evidence)

    def test_identify_devops_with_ci_cd(self):
        files = ['./.github/workflows/main.yml']
        evidence = identify_devops(files)
        self.assertIn({'type': 'CI/CD Pipeline', 'files': ['./.github/workflows/main.yml']}, evidence)

    def test_identify_devops_with_dockerfile(self):
        files = ['./Dockerfile']
        evidence = identify_devops(files)
        self.assertIn({'type': 'Containerization', 'files': ['./Dockerfile']}, evidence)

    def test_identify_devops_with_terraform(self):
        files = ['./infra/main.tf']
        evidence = identify_devops(files)
        self.assertIn({'type': 'Infrastructure-as-Code', 'files': ['./infra/main.tf']}, evidence)


class TestTaskExecutionEngine(unittest.TestCase):

    @patch('execution_engine.analyze_repository')
    @patch('execution_engine.open', new_callable=unittest.mock.mock_open, read_data="""
core_philosophy:
  principles: ['Principle 1']
methodology_protocols:
  test_driven_development:
    frictions_and_mitigations: ["TDD Rule"]
  domain_driven_design:
    frictions_and_mitigations: ["DDD Rule"]
risk_mitigation_framework:
  code_quality: ["Quality Rule"]
  security: ["Security Rule"]
    """)
    def test_ddd_warning(self, mock_open, mock_analyze):
        """Engine should issue a critical warning for tasks in a DDD core domain."""
        mock_analyze.return_value = {
            'domain_driven_design': [{'type': 'Bounded Context Detected', 'path': './core/'}]
        }
        engine = TaskExecutionEngine()
        protocols = engine.get_applicable_protocols("Modify code in ./core/domain.py")
        self.assertIn("DDD CORE DOMAIN: DDD Rule", protocols['warnings'])

    @patch('execution_engine.analyze_repository')
    @patch('execution_engine.open', new_callable=unittest.mock.mock_open, read_data="""
core_philosophy:
  principles: ['Principle 1']
methodology_protocols:
  test_driven_development:
    frictions_and_mitigations: ["TDD Rule"]
risk_mitigation_framework:
  code_quality: ["Quality Rule"]
  security: ["Security Rule"]
    """)
    def test_tdd_protocol_application(self, mock_open, mock_analyze):
        """Engine should apply TDD protocol for a new feature."""
        mock_analyze.return_value = {'test_driven_development_xp': True}
        engine = TaskExecutionEngine()
        protocols = engine.get_applicable_protocols("Implement new feature")
        self.assertIn("TDD/XP Detected: TDD Rule", protocols['methodology_specific'])

    @patch('execution_engine.analyze_repository')
    @patch('execution_engine.open', new_callable=unittest.mock.mock_open, read_data="{}")
    @patch('execution_engine.search_resources')
    @patch('execution_engine.get_abstract')
    @patch('execution_engine.get_resource_type')
    def test_dbpedia_integration(self, mock_get_resource_type, mock_get_abstract, mock_search_resources, mock_open, mock_analyze):
        """Engine should call the dbpedia client with keywords from the task."""
        mock_analyze.return_value = {}
        mock_search_resources.return_value = ["Test_Resource"]
        mock_get_abstract.return_value = "This is a test abstract."
        mock_get_resource_type.return_value = "owl:Thing"

        engine = TaskExecutionEngine()
        engine._enrich_with_domain_context("Implement a new Foobar feature.")

        mock_search_resources.assert_called_with("Foobar")
        mock_get_abstract.assert_called_with("Test_Resource")
        mock_get_resource_type.assert_called_with("Test_Resource")


if __name__ == '__main__':
    unittest.main()
