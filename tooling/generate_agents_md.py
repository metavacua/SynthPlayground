# tooling/generate_agents_md.py
import os
import importlib

def generate_agents_md():
    """
    Dynamically generates the AGENTS.md file from CHC protocols.
    """
    agents_md_content = "# Agent Protocol and Knowledge Core\\n\\n"
    agents_md_content += "This file is the central entry point for the agent's operational protocols and knowledge. It is dynamically loaded and parsed by the agent at the start of any task.\\n\\n"

    protocol_dir = "protocols/chc"
    for root, _, files in os.walk(protocol_dir):
        for file in files:
            if file == "proof.py":
                module_path = os.path.join(root, file).replace("/", ".").replace(".py", "")
                try:
                    protocol_module = importlib.import_module(module_path)
                    protocol = protocol_module.Protocol()
                    agents_md_content += f"## Protocol: {protocol.get_proposition()}\\n\\n"
                except Exception as e:
                    print(f"Error loading protocol from {module_path}: {e}")

    with open("AGENTS.md", "w") as f:
        f.write(agents_md_content)

if __name__ == "__main__":
    generate_agents_md()
