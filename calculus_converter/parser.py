import re
import json
from calculus_converter.calculus import Document

def parse_prooftree_content_final(content):
    """
    A robust, non-recursive parser for prooftree content. It extracts the
    final conclusion and all top-level hypotheses.
    """
    try:
        # The final inference is always at the end.
        # This regex captures the rule name (optional) and the conclusion text.
        infer_match = re.search(r"\\infer\d*(?:\[(.*?)\])?\{(.*?)\}\s*$", content.strip(), re.DOTALL)
        if not infer_match:
            return None

        rule_name, conclusion = infer_match.groups()
        rule_name = rule_name.strip() if rule_name else "Unknown Rule"
        conclusion = conclusion.strip()

        # To get the hypotheses, we remove the final inference from the content
        # and then find all `\hypo` commands in the remaining string.
        hypo_content = content[:infer_match.start()]
        hypotheses = re.findall(r"\\hypo\{(.*?)\}", hypo_content, re.DOTALL)

        return {
            "type": "prooftree",
            "hypotheses": [{"type": "hypo", "content": h.strip()} for h in hypotheses],
            "conclusion": conclusion,
            "rule_name": rule_name,
        }
    except Exception as e:
        print(f"Final parser failed. Error: {e}")
        return None

def cleanup_latex(text):
    """Strips the LaTeX preamble and other noisy commands."""
    text = re.sub(r"\\documentclass.*?\\begin\{document\}", "", text, flags=re.DOTALL)
    text = text.replace("\\end{document}", "")
    text = re.sub(r"\\begin\{(center|flushleft|flushright|abstract)\}", "", text)
    text = re.sub(r"\\end\{(center|flushleft|flushright|abstract)\}", "", text)
    text = re.sub(r"\\(newpage|quad|\[|\]|maketitle)", "", text)
    return text.strip()

def parse_latex_to_document(text):
    """
    Parses a LaTeX string and returns a Document object with semantic structure.
    """
    doc = Document()
    title_match = re.search(r"\\title\{(.*?)\}", text)
    doc.title = title_match.group(1) if title_match else "Untitled"
    author_match = re.search(r"\\author\{(.*?)\}", text)
    doc.author = author_match.group(1) if author_match else None

    clean_text = cleanup_latex(text)
    content_pattern = r"(\\begin{prooftree}.*?\\end{prooftree})"
    parts = re.split(content_pattern, clean_text, flags=re.DOTALL)

    for part in parts:
        if not part.strip():
            continue

        if part.startswith("\\begin{prooftree}"):
            content = part.replace("\\begin{prooftree}", "").replace("\\end{prooftree}", "").strip()
            parsed_tree = parse_prooftree_content_final(content)
            if parsed_tree:
                doc.add_proof_tree(parsed_tree)
            else:
                doc.add_element("text", f"UNPARSED PROOFTREE: {content}")
        else:
            remaining_text = part
            while remaining_text.strip():
                cmd_match = re.match(r"\s*\\(part|section|subsection|subsubsection)\{(.*?)\}", remaining_text, re.DOTALL)
                if cmd_match:
                    cmd, content = cmd_match.groups()
                    doc.add_element(cmd, content.strip())
                    remaining_text = remaining_text[cmd_match.end():]
                else:
                    next_cmd_pos = re.search(r"\\(part|section|subsection|subsubsection)\{", remaining_text)
                    if next_cmd_pos:
                        text_before = remaining_text[:next_cmd_pos.start()].strip()
                        if text_before:
                            doc.add_element("text", text_before)
                        remaining_text = remaining_text[next_cmd_pos.start():]
                    else:
                        if remaining_text.strip():
                            doc.add_element("text", remaining_text.strip())
                        break
    return doc

if __name__ == '__main__':
    with open('BS.tex', 'r') as f:
        content = f.read()

    document = parse_latex_to_document(content)

    print(document.to_json())