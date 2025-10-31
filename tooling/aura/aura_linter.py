# tooling/aura/aura_linter.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import glob
from aura_lang.lexer import Lexer
from aura_lang.parser import Parser

def lint_aura_files(files_to_lint=None):
    """
    Lints .aura files.
    """
    if files_to_lint:
        aura_files = files_to_lint
    else:
        aura_files = glob.glob("**/*.aura", recursive=True)
    errors_found = False

    for aura_file in aura_files:
        with open(aura_file, "r") as f:
            source_code = f.read()

        try:
            l = Lexer(source_code)
            p = Parser(l)
            program = p.parse_program()

            if p.errors:
                errors_found = True
                print(f"Errors found in {aura_file}:")
                for error in p.errors:
                    print(f"  - {error}")
        except Exception as e:
            errors_found = True
            print(f"Errors found in {aura_file}:")
            print(f"  - {e}")

    if errors_found:
        sys.exit(1)
    else:
        print("No errors found in .aura files.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        lint_aura_files(sys.argv[1:])
    else:
        lint_aura_files()
