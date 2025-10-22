import os
import re
from datetime import datetime
from utils.file_system_utils import get_agents_md_path


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
    log_section_regex = re.compile(
        r"(^# Jules' Action Log\n)(.*?)(^#|\Z)", re.MULTILINE | re.DOTALL
    )
    match = log_section_regex.search(content)

    log_entry = f"- {action_text}\n"

    if match:
        # Append to existing log
        new_content = content[: match.end(2)] + log_entry + content[match.end(2) :]
    else:
        # Add new log section
        new_content = content + "\n\n" + log_header + "\n\n" + log_entry

    with open(agents_md_path, "w") as f:
        f.write(new_content)
