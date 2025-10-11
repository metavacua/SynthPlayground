"""
Generates a single HTML file for GitHub Pages from the repository's metalanguage.

This script combines the human-readable `README.md` and the machine-readable
`AGENTS.md` into a single, navigable HTML document. It uses the `markdown`
library to convert the Markdown content to HTML and to automatically generate
a Table of Contents.

The final output is a semantic HTML5 document, `_site/index.html`, which serves
as the main page for the project's GitHub Pages site.
"""
import markdown
import os

# --- Configuration ---
README_PATH = "README.md"
AGENTS_MD_PATH = "AGENTS.md"
OUTPUT_DIR = "_site"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "index.html")
PAGE_TITLE = "Project Chimera: System Metalanguage"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
            line-height: 1.6;
            color: #24292e;
            max-width: 980px;
            margin: 20px auto;
            padding: 0 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            border-bottom: 1px solid #eaecef;
            padding-bottom: .3em;
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
        }}
        code, pre {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 85%;
        }}
        pre {{
            background-color: #f6f8fa;
            border-radius: 6px;
            padding: 16px;
            overflow: auto;
        }}
        code {{
            background-color: rgba(27,31,35,.05);
            border-radius: 3px;
            padding: .2em .4em;
        }}
        pre > code {{
            padding: 0;
            background-color: transparent;
        }}
        .toc {{
            background-color: #f6f8fa;
            border: 1px solid #eaecef;
            border-radius: 6px;
            padding: 10px 20px;
            margin-bottom: 30px;
        }}
        .toc ul {{
            padding-left: 20px;
        }}
        article {{
            margin-bottom: 40px;
        }}
        hr {{
            height: .25em;
            padding: 0;
            margin: 24px 0;
            background-color: #e1e4e8;
            border: 0;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
    </header>
    <main>
        <nav class="toc">
            <h2>Table of Contents</h2>
            {toc}
        </nav>
        <article>
            {body_content}
        </article>
    </main>
    <footer>
        <p><em>This page was automatically generated from the repository's source files.</em></p>
    </footer>
</body>
</html>
"""

def generate_html_page():
    """
    Reads the source Markdown files, converts them to HTML, and builds the
    final index.html page.
    """
    print("--> Reading source markdown files...")
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            readme_md = f.read()
        with open(AGENTS_MD_PATH, "r", encoding="utf-8") as f:
            agents_md = f.read()
    except FileNotFoundError as e:
        print(f"Error: Could not find a source file: {e}")
        return

    print("--> Creating combined markdown document...")

    # Combine the two markdown files into a single document string.
    # This ensures that header IDs are unique across the entire page,
    # allowing the Table of Contents to generate correct anchor links.
    full_md_content = f"""
# Human-Readable Metalanguage (README.md)
{readme_md}

<hr>

# Machine-Readable Metalanguage (AGENTS.md)
{agents_md}
"""

    print("--> Converting markdown to HTML...")
    # Convert the document *without* the TOC extension to get the body
    md_body = markdown.Markdown(extensions=['fenced_code', 'extra'])
    body_html = md_body.convert(full_md_content)

    # Convert the document *with* the TOC extension to get the TOC
    md_toc = markdown.Markdown(extensions=['toc', 'extra'])
    md_toc.convert(full_md_content)
    toc_html = md_toc.toc

    print("--> Assembling final index.html...")
    final_html = HTML_TEMPLATE.format(
        title=PAGE_TITLE,
        toc=toc_html,
        body_content=body_html
    )

    # Ensure the output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"--> Successfully generated {OUTPUT_PATH}")
    except IOError as e:
        print(f"Error: Could not write to output file {OUTPUT_PATH}: {e}")

if __name__ == "__main__":
    generate_html_page()