# tooling/lint_chc_protocols.py
import os
import importlib
import logging
import sys

# Configure logging to provide clear output about the script's execution.
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def lint_chc_protocols():
    """
    Lints all CHC protocols in the repository to ensure they are well-formed.
    This script serves as a quality gate, checking for:
    1. Successful importation of the protocol module.
    2. Presence of a 'Protocol' class.
    3. Correct implementation of the CHCProtocol interface.
    """
    logging.info("Starting CHC protocol linting.")

    protocol_dir = "protocols/chc"
    if not os.path.isdir(protocol_dir):
        logging.error(
            f"CHC protocol directory not found at '{protocol_dir}'. Aborting."
        )
        return False

    has_errors = False
    protocol_count = 0

    # Walk through the protocol directory to find all 'proof.py' files.
    for root, _, files in os.walk(protocol_dir):
        if "proof.py" in files:
            protocol_count += 1
            # Construct the Python module path from the file path.
            module_path = (
                os.path.join(root, "proof.py")
                .replace(os.path.sep, ".")
                .replace(".py", "")
            )

            try:
                # 1. Check for successful importation.
                protocol_module = importlib.import_module(module_path)
                logging.info(f"Successfully imported protocol: {module_path}")

                # 2. Check for the presence of a 'Protocol' class.
                if not hasattr(protocol_module, "Protocol"):
                    logging.error(
                        f"Protocol '{module_path}' is missing the 'Protocol' class."
                    )
                    has_errors = True
                    continue

                # 3. Check for correct implementation of the CHCProtocol interface.
                protocol_instance = protocol_module.Protocol()

                required_methods = [
                    "get_proposition",
                    "check_preconditions",
                    "check_postconditions",
                    "check_invariants",
                    "get_proof",
                    "get_initial_state",
                ]

                missing_methods = [
                    method
                    for method in required_methods
                    if not hasattr(protocol_instance, method)
                ]

                if missing_methods:
                    logging.error(
                        f"Protocol '{module_path}' is missing the following required methods: {', '.join(missing_methods)}"
                    )
                    has_errors = True
                else:
                    logging.info(
                        f"Protocol '{module_path}' correctly implements the CHCProtocol interface."
                    )

            except ImportError as e:
                logging.error(f"Failed to import protocol from '{module_path}': {e}")
                has_errors = True
            except Exception as e:
                logging.error(
                    f"An unexpected error occurred while linting protocol '{module_path}': {e}"
                )
                has_errors = True

    if has_errors:
        logging.error("CHC protocol linting failed with one or more errors.")
    elif protocol_count == 0:
        logging.warning("No CHC protocols were found to lint.")
    else:
        logging.info("All CHC protocols passed the linter.")

    return not has_errors


if __name__ == "__main__":
    if not lint_chc_protocols():
        sys.exit(1)
