import argparse
import os
import sys

# This is a hack to get the tooling directory in the path
# It must happen before the local imports.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from tooling.master_control import MasterControlGraph
from tooling.state import AgentState


def main():
    """Sets up the environment and runs the FDC agent."""
    load_dotenv()  # Load environment variables from .env file

    parser = argparse.ArgumentParser(description="Run the FDC agent.")
    parser.add_argument("task", type=str, help="The task for the agent to perform.")
    args = parser.parse_args()

    initial_state = AgentState(task=args.task)
    master_control = MasterControlGraph(initial_state)
    master_control.run()


if __name__ == "__main__":
    main()
