import os
from jinja2 import Environment, FileSystemLoader
from calculus_converter.generator import generate_html

def convert_all_latex_files(root_dir=".", output_dir="."):
    """
    Finds all .tex files in the root directory, converts them to HTML,
    and generates an index file for the converted documents.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    converted_files = []
    for filename in sorted(os.listdir(root_dir)):
        if filename.endswith(".tex"):
            latex_filepath = os.path.join(root_dir, filename)
            print(f"Converting {latex_filepath}...")
            try:
                # generate_html returns the title and output filename
                title, output_filename = generate_html(latex_filepath, output_dir)
                converted_files.append({"title": title, "filename": output_filename})
            except Exception as e:
                print(f"  Error converting {filename}: {e}")

    # Now, generate the index page
    print("\nGenerating index page...")
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('calculus_index.html')

    index_html_content = template.render(files=converted_files)

    index_filepath = os.path.join(output_dir, 'index.html')
    with open(index_filepath, 'w') as f:
        f.write(index_html_content)
    print(f"Successfully generated {index_filepath}")


if __name__ == '__main__':
    output_directory = 'converted_calculus'
    convert_all_latex_files('.', output_directory)
    print("\nConversion process complete.")