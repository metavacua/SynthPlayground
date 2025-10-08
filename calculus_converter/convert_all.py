import os
from calculus_converter.generator import generate_html

def convert_all_latex_files(root_dir=".", output_dir="."):
    """
    Finds all .tex files in the root directory and converts them to HTML.
    """
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(root_dir):
        if filename.endswith(".tex"):
            latex_filepath = os.path.join(root_dir, filename)
            print(f"Converting {latex_filepath}...")
            try:
                generate_html(latex_filepath, output_dir)
            except Exception as e:
                print(f"  Error converting {filename}: {e}")

if __name__ == '__main__':
    # Create a dedicated output directory for the HTML files
    output_directory = 'converted_calculus'
    convert_all_latex_files('.', output_directory)
    print("\nConversion process complete.")