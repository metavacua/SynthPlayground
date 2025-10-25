def generate_command_from_plan_step(cmd, outputs):
    """
    Generates a command to be executed from a plan step.
    """
    tool_name = cmd.tool_name
    arguments = cmd.args_text

    # Substitute outputs from previous steps.
    for key, value in outputs.items():
        arguments = arguments.replace(f"<{key}>", value)

    if tool_name == "run_in_bash_session":
        return arguments
    elif tool_name == "refactor":
        return f"python3 tooling/refactor.py {arguments}"
    elif tool_name == "create_file":
        return f"python3 tooling/custom_tools/create_file.py {arguments}"
    elif tool_name == "read_file":
        return f"python3 tooling/custom_tools/read_file.py {arguments}"
    elif tool_name == "fetch_data":
        return f"python3 tooling/custom_tools/fetch_data.py {arguments}"
    elif tool_name == "analyze_data":
        return f"python3 tooling/custom_tools/analyze_data.py {arguments}"
    else:
        return None
