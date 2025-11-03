"""
This tool simulates a call to an external LLM service.
It serves as the formal interface for the CRE agent to delegate tasks that
require natural language understanding or creative code generation.
"""

import argparse
import json
import sys

def simulate_llm_call(prompt: str) -> dict:
    """
    Simulates an LLM call by returning a pre-defined response for a specific prompt.
    """
    # This is the specific prompt we will look for in our demonstration.
    memoization_prompt = "Refactor this function to be more efficient by using a memoization cache."

    if memoization_prompt in prompt:
        # If the prompt matches, return a structured JSON response containing the
        # refactored code, as if an LLM had generated it.
        refactored_code = """
import functools

@functools.lru_cache(maxsize=None)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
        return {
            "status": "SUCCESS",
            "refactored_code": refactored_code.strip()
        }
    else:
        # For any other prompt, return a generic "I don't know" response.
        return {
            "status": "FAILURE",
            "error": "The simulated LLM could not handle this prompt."
        }

import uuid
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import Logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Simulated LLM Service Tool.")
    parser.add_argument("prompt", help="The natural language prompt to send to the LLM.")
    parser.add_argument("--session-id", required=False, help="The session ID, provided by a parent agent.")
    args = parser.parse_args()

    session_id = args.session_id if args.session_id else str(uuid.uuid4())
    logger = Logger(session_id=session_id)

    action_details = {
        "tool": "llm_service.py",
        "prompt": args.prompt
    }

    try:
        response = simulate_llm_call(args.prompt)

        logger.log(
            phase="Phase 3",
            task_id="llm_service_task", # This tool doesn't have a task_id
            plan_step=-1,
            action_type="TOOL_EXEC",
            action_details=action_details,
            outcome_status="SUCCESS",
            outcome_message="LLM call simulated successfully."
        )

        print(json.dumps(response, indent=2))

    except Exception as e:
        logger.log(
            phase="Phase 3",
            task_id="llm_service_task",
            plan_step=-1,
            action_type="TOOL_EXEC",
            action_details=action_details,
            outcome_status="FAILURE",
            error_details={"error": str(e)}
        )
        sys.exit(1)
