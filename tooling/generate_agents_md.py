# tooling/generate_agents_md.py
import os
import importlib
import logging

# Configure logging to provide clear output about the script's execution.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def generate_agents_md():
    """
    Dynamically generates the AGENTS.md file from CHC protocols.
    This script is designed to be a total function, meaning it will always produce a valid
    AGENTS.md file even if some protocol files are malformed. It achieves this by
    gracefully handling import and instantiation errors for individual protocols.
    """
    logging.info("Starting AGENTS.md generation.")

    agents_md_content = "# Agent Protocol and Knowledge Core\\n\\n"
    agents_md_content += "This file is the central entry point for the agent's operational protocols and knowledge. It is dynamically generated from the verifiable CHC protocol modules.\\n\\n"

    protocol_dir = "protocols/chc"
    if not os.path.isdir(protocol_dir):
        logging.warning(
            f"CHC protocol directory not found at '{protocol_dir}'. No protocols will be listed."
        )

    verified_protocols = []

    # Walk through the protocol directory to find all 'proof.py' files.
    for root, _, files in os.walk(protocol_dir):
        if "proof.py" in files:
            # Construct the Python module path from the file path.
            module_path = (
                os.path.join(root, "proof.py")
                .replace(os.path.sep, ".")
                .replace(".py", "")
            )

            try:
                # Dynamically import the protocol module.
                protocol_module = importlib.import_module(module_path)

                # Instantiate the protocol class defined within the module.
                protocol = protocol_module.Protocol()

                # Get the proposition and add it to our list for later processing.
                proposition = protocol.get_proposition()
                verified_protocols.append(proposition)
                logging.info(f"Successfully loaded protocol: {proposition}")

            except ImportError as e:
                logging.error(f"Failed to import protocol from '{module_path}': {e}")
            except AttributeError as e:
                logging.error(
                    f"Protocol in '{module_path}' is malformed (e.g., missing 'Protocol' class or required methods): {e}"
                )
            except Exception as e:
                logging.error(
                    f"An unexpected error occurred while loading protocol from '{module_path}': {e}"
                )

    # Sort the protocols alphabetically to ensure the output is deterministic.
    if verified_protocols:
        verified_protocols.sort()
        for proposition in verified_protocols:
            agents_md_content += f"- **{proposition}**\\n"
    else:
        agents_md_content += "*No CHC-verified protocols found or loaded.*\\n"

    # Write the final, combined content to the AGENTS.md file in the root directory.
    try:
        with open("AGENTS.md", "w") as f:
            f.write(agents_md_content)
        logging.info("Successfully generated AGENTS.md.")
    except IOError as e:
        logging.error(f"Failed to write to AGENTS.md: {e}")


if __name__ == "__main__":
    generate_agents_md()
