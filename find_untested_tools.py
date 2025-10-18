import os

tooling_dir = "tooling"
tool_files = [f for f in os.listdir(tooling_dir) if f.endswith(".py") and not f.startswith("test_") and not f.startswith("__")]
test_files = [f for f in os.listdir(tooling_dir) if f.startswith("test_")]

untested_tools = []
for tool_file in tool_files:
    test_file_name = f"test_{tool_file}"
    if test_file_name not in test_files:
        untested_tools.append(tool_file)

if untested_tools:
    print("Untested tools:")
    for tool in untested_tools:
        print(f"- {tool}")
else:
    print("All tools have corresponding test files.")
