# protocols/core/conditional_refactoring.protocol.py

PROTOCOL_ID = "core-conditional-refactoring-001"
DESCRIPTION = "A protocol that applies specific refactoring guidelines only when working on the 'legacy' module."
ASSOCIATED_TOOLS = ["tooling/refactor.py"]


def is_applicable(context):
    """
    This protocol is only applicable if the task is 'refactor' and
    at least one of the target files is within the 'legacy/' directory.
    """
    if context.get("task_type") != "refactor":
        return False

    target_files = context.get("target_files", [])
    if not target_files:
        return False

    for f in target_files:
        if "legacy/" in f:
            return True

    return False


RULES = [
    {
        "rule_id": "cr-001",
        "description": "When refactoring legacy code, prioritize replacing deprecated function calls with their modern equivalents as defined in the 'Modernization Guide'.",
        "enforcement": "The 'refactor.py' tool will cross-reference changes against a list of known deprecated functions when operating in legacy mode.",
    },
    {
        "rule_id": "cr-002",
        "description": (
            lambda context: f"A special review by the 'Legacy Systems Team' must be requested for the following files: {', '.join(context.get('target_files', []))}"
        ),
        "enforcement": "Procedural. The agent must explicitly tag the 'Legacy Systems Team' in the pull request description.",
    },
]
