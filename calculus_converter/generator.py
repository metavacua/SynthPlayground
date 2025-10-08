import os
from jinja2 import Environment, FileSystemLoader
from calculus_converter.parser import parse_latex_to_document

def generate_html(latex_filepath, output_dir="."):
    """
    Generates an HTML file from a LaTeX file.
    """
    # Set up Jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('document.html')

    # Read and parse the LaTeX file
    with open(latex_filepath, 'r') as f:
        content = f.read()

    document = parse_latex_to_document(content)

    # Prepare data for the template
    base_name = os.path.basename(latex_filepath)
    title = os.path.splitext(base_name)[0]

    # The document object now has the title, so we can use it.
    if document.title == "Untitled":
        document.title = title.replace('_', ' ').title()

    template_data = {
        "document": document
    }

    # Render the HTML
    html_content = template.render(template_data)

    # Write the output file
    output_filename = f"{title}.html"
    output_filepath = os.path.join(output_dir, output_filename)

    with open(output_filepath, 'w') as f:
        f.write(html_content)

    print(f"Successfully generated {output_filepath}")

if __name__ == '__main__':
    # Convert IdentityCalculus.tex as a test case
    output_dir = 'converted_calculus'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    generate_html('IdentityCalculus.tex', output_dir)