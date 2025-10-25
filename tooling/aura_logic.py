import subprocess
import sys
from pathlib import Path
from aura_lang.interpreter import Object


def dynamic_agent_call_tool(tool_name_obj: Object, *args: Object) -> Object:
    """
    Dynamically imports and calls a tool from the 'tooling' directory and wraps the result.

    This function provides the bridge between the Aura scripting environment and the
    Python-based agent tools. It takes the tool's module name and arguments,
    runs the tool in a subprocess, and wraps the captured output in an Aura `Object`.

    Args:
        tool_name_obj: An Aura Object containing the tool's module name (e.g., 'hdl_prover').
        *args: A variable number of Aura Objects to be passed as string arguments to the tool.

    Returns:
        An Aura `Object` containing the tool's stdout as a string, or an error message.
    """
    try:
        tool_name = tool_name_obj.value
        unwrapped_args = [str(arg.value) for arg in args]

        # --- Internal Python Tools ---
        if tool_name == "setup_planning":
            import planning
            domain_file = unwrapped_args[0]
            initial_state_fluents = unwrapped_args[1].split(',')
            planning.load_domain(domain_file)
            planning.create_state(initial_state_fluents)
            return Object("OK")

        elif tool_name == "find_plan":
            import planning
            goal_conditions = unwrapped_args[0].split(',')
            plan = planning.find_plan(goal_conditions)
            if plan is not None:
                return Object(",".join(plan))
            else:
                return Object("Error: No plan found")

        # --- External Subprocess Tools ---
        else:
            # Sanitize the tool_name to prevent directory traversal vulnerabilities.
            if ".." in tool_name or "/" in tool_name:
                raise ValueError("Invalid tool name format.")

            tool_module_path = Path(__file__).resolve().parent / f"{tool_name}.py"
            if not tool_module_path.exists():
                raise ModuleNotFoundError(
                    f"Tool '{tool_name}' not found at '{tool_module_path}'"
                )

            command = [sys.executable, str(tool_module_path)] + unwrapped_args
            print(f"[Aura Executor]: Calling tool '{tool_name}' with args: {unwrapped_args}")
            result = subprocess.run(command, capture_output=True, text=True, check=False)

            if result.returncode != 0:
                error_output = result.stderr.strip()
                print(f"Error calling tool '{tool_name}': {error_output}", file=sys.stderr)
                return Object(f"Error: {error_output}")

            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip(), file=sys.stderr)

            return Object(result.stdout.strip())

    except Exception as e:
        error_msg = f"An unexpected error occurred when calling tool '{tool_name_obj.value}': {e}"
        print(error_msg, file=sys.stderr)
        return Object(f"Error: {error_msg}")
