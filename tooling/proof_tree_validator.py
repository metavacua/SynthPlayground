import os
import json
import glob

# The set of all tools that are considered 'axiomatic' or 'built-in' to the agent's execution environment.
# A 'closed' protocol branch is only allowed to depend on tools from this set.
AXIOMATIC_TOOLS = {
    "read_file",
    "list_files",
    "create_file_with_block",
    "overwrite_file_with_block",
    "replace_with_git_merge_diff",
    "delete_file",
    "rename_file",
    "run_in_bash_session",
    "google_search",
    "view_text_website",
    "set_plan",
    "plan_step_complete",
    "message_user",
    "request_user_input",
    "record_user_approval_for_plan",
    "request_code_review",
    "submit",
    "reset_all",
    "restore_file",
    "grep",
    "view_image",
    "read_image_file",
    "frontend_verification_instructions",
    "frontend_verification_complete",
    "pre_commit_instructions",
    "initiate_memory_recording",
    "read_pr_comments",
    "reply_to_pr_comments",
}

def validate_proof_tree(root_dir="."):
    """
    Scans all protocol files and validates the integrity of the 'proof tree'.
    Specifically, it ensures that any protocol marked with 'branch_status: closed'
    only depends on tools from the AXIOMATIC_TOOLS set.
    """
    print("--- Running Proof Tree Validator ---")
    all_protocol_files = glob.glob(os.path.join(root_dir, "**/*.protocol.json"), recursive=True)

    errors_found = 0

    for file_path in all_protocol_files:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                protocol_data = json.loads(content)
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {file_path}")
            errors_found += 1
            continue

        if protocol_data.get("branch_status") == "closed":
            protocol_id = protocol_data.get("protocol_id", "N/A")

            # Check top-level associated_tools
            associated_tools = protocol_data.get("associated_tools", [])
            non_axiomatic_tools = set(associated_tools) - AXIOMATIC_TOOLS

            if non_axiomatic_tools:
                print(f"\n!!! Proof Tree Error in protocol: {protocol_id} ({file_path})")
                print("  This protocol is marked as 'closed', but depends on the following non-axiomatic tools:")
                for tool in sorted(list(non_axiomatic_tools)):
                    print(f"    - {tool}")
                errors_found += 1

            # Check associated_tools within rules
            for rule in protocol_data.get("rules", []):
                rule_id = rule.get("rule_id", "N/A")
                associated_tools = rule.get("associated_tools", [])
                non_axiomatic_tools = set(associated_tools) - AXIOMATIC_TOOLS

                if non_axiomatic_tools:
                    print(f"\n!!! Proof Tree Error in protocol: {protocol_id}, rule: {rule_id} ({file_path})")
                    print("  This protocol is marked as 'closed', but a rule within it depends on the following non-axiomatic tools:")
                    for tool in sorted(list(non_axiomatic_tools)):
                        print(f"    - {tool}")
                    errors_found += 1

    if errors_found > 0:
        print(f"\nValidation failed: Found {errors_found} error(s) in the proof tree.")
        exit(1)
    else:
        print("\n--- Proof Tree Validation Successful ---")
        print("All 'closed' protocols adhere to axiomatic dependencies.")

if __name__ == "__main__":
    validate_proof_tree()