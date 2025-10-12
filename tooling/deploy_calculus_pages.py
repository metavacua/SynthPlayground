import os
import shutil

def deploy_calculus_pages():
    """
    Deploys the converted calculus HTML files to a directory suitable for
    GitHub Pages.
    """
    source_dir = 'converted_calculus'
    output_dir = 'gh-pages'

    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' not found.")
        print("Please run the calculus converter first.")
        return

    # Create or clean the output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Copy all files from the source to the output directory
    for filename in os.listdir(source_dir):
        source_path = os.path.join(source_dir, filename)
        if os.path.isfile(source_path):
            shutil.copy(source_path, output_dir)

    print(f"Successfully deployed calculus pages to '{output_dir}' directory.")

if __name__ == '__main__':
    deploy_calculus_pages()