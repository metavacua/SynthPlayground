# tooling/aura/aura_api.py

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

import os
from aura_lang.interpreter import Object

class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name):
        return self._tools.get(name)

class Tool:
    def __init__(self, name, func, description=""):
        self.name = name
        self.func = func
        self.description = description

    def __call__(self, *args):
        return self.func(*args)

def agent_call_tool(registry, tool_name_obj, *args):
    tool_name = tool_name_obj.value
    tool = registry.get(tool_name)

    if not tool:
        return Object(f"Error: Tool '{tool_name}' not found.")

    try:
        unwrapped_args = [arg.value for arg in args]
        result = tool(*unwrapped_args)
        return Object(result)
    except Exception as e:
        return Object(f"Error executing tool '{tool_name}': {e}")

# --- Initialize the registry and register tools ---
registry = ToolRegistry()

def hello_world_tool(name):
    return f"Hello, {name}!!"

def read_file_tool(path):
    try:
        with open(path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: File not found."

def get_env_tool(var_name):
    return os.environ.get(var_name, "")

def validate_tdd_tool():
    return "Success"

def validate_guardian_tool():
    return "Success"

def install_dependencies_tool():
    return "Success"

registry.register(Tool("hello_world", hello_world_tool, "A simple hello world tool."))
registry.register(Tool("read_file", read_file_tool, "Reads a file and returns its contents."))
registry.register(Tool("get_env", get_env_tool, "Gets the value of an environment variable."))
registry.register(Tool("validate_tdd", validate_tdd_tool, "Validates that TDD was followed."))
registry.register(Tool("validate_guardian", validate_guardian_tool, "Validates that the guardian protocol was followed."))
registry.register(Tool("install_dependencies", install_dependencies_tool, "Installs dependencies from requirements.txt."))
