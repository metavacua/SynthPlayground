"""
A command-line tool for initiating a new self-improvement proposal.

This script is the entry point for the Self-Improvement Protocol (SIP). It
automates the boilerplate process of creating a new proposal, ensuring that all
proposals are structured correctly and stored in a consistent location.

When executed, this tool will:
1.  Create a new, timestamped directory within the `proposals/` directory to
    house the new proposal.
2.  Generate a `proposal.md` file within that new directory.
3.  Populate the `proposal.md` with a standard template that includes all the
    required sections as defined in the Self-Improvement Protocol (rule sip-002).
4.  Print the path to the newly created proposal file, so the agent can
    immediately begin editing it.
"""

import argparse
import os
import datetime

# --- Configuration ---
PROPOSALS_DIR = "proposals"
PROPOSAL_TEMPLATE = """\
# Self-Improvement Proposal

## 1. Problem Statement
*(Describe the problem, inefficiency, or bug that this proposal aims to address.
Provide evidence, such as links to log entries or test failures.)*

...

## 2. Proposed Solution
*(Provide a detailed description of the proposed change. This should include
any modifications to code, protocols, or documentation.)*

...

## 3. Success Criteria
*(How will we know if this change is successful? Define specific, measurable
outcomes. This must include references to specific tests or verification
scripts that will be used to validate the change.)*

...

## 4. Impact Analysis
*(What is the potential impact of this change? Consider effects on performance,
security, and other agent protocols.)*

...
"""


def create_proposal():
    """
    Creates a new, structured proposal for self-improvement.
    """
    # Create the base proposals directory if it doesn't exist
    os.makedirs(PROPOSALS_DIR, exist_ok=True)
    os.makedirs("reviews", exist_ok=True)

    # Generate a unique directory name for the new proposal
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    proposal_dir_name = f"sip-{timestamp}"
    proposal_dir_path = os.path.join(PROPOSALS_DIR, proposal_dir_name)
    os.makedirs(proposal_dir_path)

    # Create and populate the proposal.md file
    proposal_file_path = os.path.join(proposal_dir_path, "proposal.md")
    with open(proposal_file_path, "w") as f:
        f.write(PROPOSAL_TEMPLATE)

    review_file_path = os.path.join("reviews", f"{proposal_dir_name}.md")
    review_template = """\
# Guardian Protocol Review

## Summary

...

## Impact Analysis

...

## Verification Plan

...
"""
    with open(review_file_path, "w") as f:
        f.write(review_template)


    print(f"Successfully created new proposal at: {proposal_file_path}")
    print(f"Successfully created new review document at: {review_file_path}")
    return proposal_file_path


def main():
    """
    Main function to run the self-improvement proposal generator.
    """
    parser = argparse.ArgumentParser(
        description="Initiates a new self-improvement proposal."
    )
    # This tool is simple and doesn't need arguments for now, but the
    # parser is here for future extensibility.
    args = parser.parse_args()

    create_proposal()


if __name__ == "__main__":
    main()
