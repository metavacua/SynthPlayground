"""
Generates a single HTML file for GitHub Pages from the repository's metalanguage.

This script combines the human-readable `README.md` and the machine-readable
`AGENTS.md` into a single, navigable HTML document. It uses the `markdown`
library to convert the Markdown content to HTML and to automatically generate
a Table of Contents.

The final output is a semantic HTML5 document, `index.html`, which serves as
the main page for the project's GitHub Pages site.
"""

import markdown

# --- Configuration ---
README_PATH = "README.md"
AGENTS_MD_PATH = "AGENTS.md"
OUTPUT_PATH = "index.html"
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
            list-style-type: none;
        }}
        .toc li {{
            margin-top: 4px;
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
        {body_content}
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
    # Use the `md_in_html` extension by wrapping content in `article` tags
    # with the `markdown="1"` attribute. This allows us to process the
    # whole document at once, ensuring the TOC and header IDs are consistent.
    full_md_content = f"""
<article id="readme" markdown="1">
<h2>Human-Readable Metalanguage (README.md)</h2>

{readme_md}
</article>

<hr>

<article id="agents-md" markdown="1">
<h2>Machine-Readable Metalanguage (AGENTS.md)</h2>

{agents_md}
</article>
"""

    print("--> Converting combined markdown to HTML with TOC...")
    # 'toc' for table of contents, 'fenced_code' for code blocks,
    # 'extra' for features like tables, and 'md_in_html' to process
    # markdown inside the article tags.
    md = markdown.Markdown(extensions=["toc", "fenced_code", "extra", "md_in_html"])

    body_html = md.convert(full_md_content)
    toc_html = md.toc

    print("--> Assembling final index.html...")
    final_html = HTML_TEMPLATE.format(
        title=PAGE_TITLE, toc=toc_html, body_content=body_html
    )

    try:
        with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
            f.write(final_html)
        print(f"--> Successfully generated {OUTPUT_PATH}")
    except IOError as e:
        print(f"Error: Could not write to output file {OUTPUT_PATH}: {e}")


if __name__ == "__main__":
    generate_html_page()
