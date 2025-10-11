import re
import json
from calculus_converter.calculus import Document

def find_top_level_commands(text):
    """Finds top-level \hypo and \infer commands, respecting nested braces."""
    commands = []
    i = 0
    while i < len(text):
        match = re.search(r"\\(hypo|infer\d*)", text[i:])
        if not match:
            break

        i += match.end()
        cmd_name = match.group(1)
        rule_name = None

        if cmd_name.startswith("infer"):
            rule_match = re.match(r"\s*\[(.*?)\]", text[i:])
            if rule_match:
                rule_name = rule_match.group(1)
                i += rule_match.end()

        open_brace = text.find('{', i)
        if open_brace == -1: continue

        brace_level = 1
        j = open_brace + 1
        while j < len(text):
            if text[j] == '{': brace_level += 1
            elif text[j] == '}': brace_level -= 1

            if brace_level == 0:
                content = text[open_brace+1:j]
                commands.append({'command': cmd_name, 'rule': rule_name, 'content': content})
                break
            j += 1
        i = j + 1
    return commands

def parse_prooftree_content_recursive(text):
    """A robust recursive parser for prooftree content."""
    commands = find_top_level_commands(text)
    if not commands:
        return None

    last_command = commands[-1]
    conclusion = last_command['content']
    rule_name = last_command['rule'] if last_command['rule'] else "Unknown Rule"

    hypotheses = []
    for cmd_data in commands[:-1]:
        if cmd_data['command'] == "hypo":
            content = cmd_data['content']
            if content.strip().startswith(r"\begin{prooftree}"):
                nested_content = content.strip()[17:-18]
                hypotheses.append(parse_prooftree_content_recursive(nested_content))
            else:
                hypotheses.append({"type": "hypo", "content": content})

    return {
        "type": "prooftree",
        "hypotheses": hypotheses,
        "conclusion": conclusion,
        "rule_name": rule_name
    }

def cleanup_latex(text):
    """Strips the LaTeX preamble and other noisy commands."""
    text = re.sub(r"\\documentclass.*?\\begin\{document\}", "", text, flags=re.DOTALL)
    text = text.replace("\\end{document}", "")
    text = re.sub(r"\\begin\{(center|flushleft|flushright|abstract)\}", "", text)
    text = re.sub(r"\\end\{(center|flushleft|flushright|abstract)\}", "", text)
    text = re.sub(r"\\(newpage|quad|\[|\]|maketitle)", "", text)
    return text.strip()

def find_top_level_environments(text, env_name="prooftree"):
    """Finds top-level environments (e.g., prooftree), respecting nesting."""
    begin_tag = f"\\begin{{{env_name}}}"
    end_tag = f"\\end{{{env_name}}}"

    parts = []
    level = 0
    start_of_env = 0
    last_pos = 0

    i = 0
    while i < len(text):
        if text[i:].startswith(begin_tag):
            if level == 0:
                if i > last_pos:
                    parts.append({'type': 'text', 'content': text[last_pos:i]})
                start_of_env = i
            level += 1
            i += len(begin_tag)
        elif text[i:].startswith(end_tag):
            level -= 1
            if level == 0:
                content = text[start_of_env + len(begin_tag):i].strip()
                parts.append({'type': env_name, 'content': content})
                last_pos = i + len(end_tag)
            i += len(end_tag)
        else:
            i += 1

    if last_pos < len(text):
        parts.append({'type': 'text', 'content': text[last_pos:]})

    return parts

def parse_latex_to_document(text):
    """
    Parses a LaTeX string and returns a Document object with semantic structure.
    This version correctly handles nested environments.
    """
    doc = Document()
    title_match = re.search(r"\\title\{(.*?)\}", text)
    doc.title = title_match.group(1) if title_match else "Untitled"
    author_match = re.search(r"\\author\{(.*?)\}", text)
    doc.author = author_match.group(1) if author_match else None

    clean_text = cleanup_latex(text)

    parts = find_top_level_environments(clean_text, "prooftree")

    for part in parts:
        content = part['content'].strip()
        if not content:
            continue

        if part['type'] == "prooftree":
            parsed_tree = parse_prooftree_content_recursive(content)
            if parsed_tree:
                doc.add_proof_tree(parsed_tree)
            else:
                doc.add_element("text", f"UNPARSED PROOFTREE: {content}")

        elif part['type'] == "text":
            remaining_text = content
            while remaining_text.strip():
                cmd_match = re.match(r"\s*\\(part|section|subsection|subsubsection)\{(.*?)\}", remaining_text, re.DOTALL)
                if cmd_match:
                    cmd, cmd_content = cmd_match.groups()
                    doc.add_element(cmd, cmd_content.strip())
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