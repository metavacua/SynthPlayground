# protocols/aal_spec/build.py

import os

def build(output_path):
    # This protocol is simple: it just appends the AAL spec to the AGENTS.md file.
    spec_path = os.path.join(os.path.dirname(__file__), 'definition.md')
    with open(spec_path, 'r') as f:
        spec_content = f.read()

    with open(output_path, 'a') as f:
        f.write('\\n---\\n')
        f.write(spec_content)
