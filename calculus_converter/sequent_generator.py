import os
import json
from jinja2 import Environment, FileSystemLoader
from calculus_converter.parser import parse_latex_to_document

def to_json_filter(value):
    """A custom Jinja2 filter to convert a Python object to a JSON string."""
    return json.dumps(value)

def generate_sequent_yaml(latex_filepath, output_dir="."):
    """
    Generates a structured AGENTS.md YAML file from a LaTeX file.
    """
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    env.filters['tojson'] = to_json_filter
    template = env.get_template('sequent.yml.j2')

    # Read and parse the LaTeX file
    with open(latex_filepath, 'r') as f:
        content = f.read()

    document = parse_latex_to_document(content)

    # Prepare data for the template
    base_name = os.path.splitext(os.path.basename(latex_filepath))[0]
    if document.title == "Untitled":
        document.title = base_name.replace('_', ' ').title()

    template_data = {
        "document": document
    }

    # Render the YAML content
    yaml_content = template.render(template_data)

    # Write the output file
    output_filename = f"{base_name}.agents.md"
    output_filepath = os.path.join(output_dir, output_filename)

    with open(output_filepath, 'w') as f:
        f.write(yaml_content)

    print(f"Successfully generated sequent: {output_filepath}")
    return document.title, output_filename

if __name__ == '__main__':
    # Convert IdentityCalculus.tex as a test case
    output_dir = 'sequents'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    generate_sequent_yaml('IdentityCalculus.tex', output_dir)