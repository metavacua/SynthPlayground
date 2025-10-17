import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lfi_ill.parser import parser

# This script does nothing but build the parser.
# The act of building it will cause ply to print the shift/reduce conflicts.
print("Building parser to check for conflicts...")
# The parser is built when the module is imported, but we can be explicit.
if parser:
    print("Parser built successfully.")
    print("Check the terminal output for shift/reduce conflict warnings.")
else:
    print("Parser failed to build.")