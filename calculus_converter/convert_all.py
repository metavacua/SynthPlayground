import os
import argparse
from jinja2 import Environment, FileSystemLoader
from calculus_converter.generator import generate_html
from calculus_converter.sequent_generator import generate_sequent_yaml

def convert_all_to_html(root_dir=".", output_dir="."):
    """
    Finds all .tex files in the root directory, converts them to HTML,
    and generates an index file for the converted documents.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    converted_files = []
    for filename in sorted(os.listdir(root_dir)):
        if filename.endswith(".tex"):
            latex_filepath = os.path.join(root_dir, filename)
            print(f"Converting {latex_filepath} to HTML...")
            try:
                title, output_filename = generate_html(latex_filepath, output_dir)
                converted_files.append({"title": title, "filename": output_filename})
            except Exception as e:
                print(f"  Error converting {filename}: {e}")

    # Generate the index page
    print("\nGenerating HTML index page...")
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('calculus_index.html')
    index_html_content = template.render(files=converted_files)
    index_filepath = os.path.join(output_dir, 'index.html')
    with open(index_filepath, 'w') as f:
        f.write(index_html_content)
    print(f"Successfully generated {index_filepath}")

def convert_all_to_sequents(root_dir=".", output_dir="."):
    """
    Finds all .tex files in the root directory and converts them to structured
    AGENTS.md sequent files.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in sorted(os.listdir(root_dir)):
        if filename.endswith(".tex"):
            latex_filepath = os.path.join(root_dir, filename)
            print(f"Converting {latex_filepath} to Sequent...")
            try:
                generate_sequent_yaml(latex_filepath, output_dir)
            except Exception as e:
                print(f"  Error converting {filename} to sequent: {e}")

def main():
    """Main function to drive the conversion process."""
    parser = argparse.ArgumentParser(
        description="Convert LaTeX calculus files to other formats."
    )
    parser.add_argument(
        '--format',
        choices=['html', 'sequents'],
        default='html',
        help="The output format: 'html' for documentation, 'sequents' for AGENTS.md files."
    )
    parser.add_argument(
        '--root-dir',
        default='.',
        help="The directory to scan for .tex files."
    )
    parser.add_argument(
        '--output-dir',
        help="The directory to save the output files."
    )
    args = parser.parse_args()

    if args.format == 'html':
        output_dir = args.output_dir or 'converted_calculus'
        convert_all_to_html(args.root_dir, output_dir)
    elif args.format == 'sequents':
        output_dir = args.output_dir or 'sequents'
        convert_all_to_sequents(args.root_dir, output_dir)

    print("\nConversion process complete.")

if __name__ == '__main__':
    main()