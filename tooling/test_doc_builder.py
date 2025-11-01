import unittest
from tooling.doc_builder_logic import (
    parse_file_for_docs,
)


class TestDocBuilder(unittest.TestCase):
    def test_parse_file_for_docs(self):
        content = '''"""This is a module docstring."""
class MyClass:
    """This is a class docstring."""
    def my_method(self):
        """This is a method docstring."""
        pass

def my_function():
    """This is a function docstring."""
    pass
'''
        module_doc = parse_file_for_docs("my_module.py", content)
        self.assertEqual(module_doc.docstring, "This is a module docstring.")
        self.assertEqual(len(module_doc.classes), 1)
        self.assertEqual(len(module_doc.functions), 1)
        self.assertEqual(module_doc.classes[0].name, "MyClass")
        self.assertEqual(module_doc.functions[0].name, "my_function")


if __name__ == "__main__":
    unittest.main()
