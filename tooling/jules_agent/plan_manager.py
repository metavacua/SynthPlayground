"""
This module provides functionality for...
"""

import os
import re
from utils.file_system_utils import get_agents_md_path


def inject_plan(plan_text, cwd):
    """Injects or updates the plan in the AGENTS.md file."""
    agents_md_path = get_agents_md_path(cwd)
    if not agents_md_path:
        # Create AGENTS.md if it doesn't exist
        with open(os.path.join(cwd, "AGENTS.md"), "w") as f:
            f.write("# Jules' Plan\n\n" + plan_text)
        return

    with open(agents_md_path, "r") as f:
        content = f.read()

    plan_header = "# Jules' Plan"
    plan_section_regex = re.compile(
        r"(^# Jules' Plan\n)(.*?)(^#|\Z)", re.MULTILINE | re.DOTALL
    )
    match = plan_section_regex.search(content)

    if match:
        # Update existing plan
        new_content = content.replace(match.group(2), "\n" + plan_text + "\n\n")
    else:
        # Add new plan section
        new_content = content + "\n\n" + plan_header + "\n\n" + plan_text

    with open(agents_md_path, "w") as f:
        f.write(new_content)
