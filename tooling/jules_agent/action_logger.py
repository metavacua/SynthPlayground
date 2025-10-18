import os
import re
from datetime import datetime

def get_agents_md_path(cwd):
    """Finds the AGENTS.md file in the given directory."""
    path = os.path.join(cwd, "AGENTS.md")
    if os.path.exists(path):
        return path
    return None

def log_action(action_text, cwd):
    """Logs an action to the AGENTS.md file."""
    agents_md_path = get_agents_md_path(cwd)
    if not agents_md_path:
        # Create AGENTS.md if it doesn't exist
        with open(os.path.join(cwd, "AGENTS.md"), "w") as f:
            f.write("# Jules' Action Log\n\n- " + action_text)
        return

    with open(agents_md_path, "r") as f:
        content = f.read()

    log_header = "# Jules' Action Log"
    log_section_regex = re.compile(r"(^# Jules' Action Log\n)(.*?)(^#|\Z)", re.MULTILINE | re.DOTALL)
    match = log_section_regex.search(content)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"- {timestamp}: {action_text}\n"

    if match:
        # Append to existing log
        new_content = content.replace(match.group(2), match.group(2) + log_entry)
    else:
        # Add new log section
        new_content = content + "\n\n" + log_header + "\n\n" + log_entry

    with open(agents_md_path, "w") as f:
        f.write(new_content)
