"""
A centralized registry for all agent-callable tools.

This module provides a single source of truth for tool discovery, mapping
tool names to their corresponding modules. This avoids hardcoding tool paths
and allows for a more scalable and maintainable toolchain.
"""

# The registry is a dictionary mapping the tool name (as used in plans)
# to the Python module that implements it.
TOOL_REGISTRY = {
    "hdl_prover": "tooling.hdl_prover",
    "environmental_probe": "tooling.environmental_probe",
    "logic_system_verifier": "tooling.logic_system_verifier",
    # Add other tools here as they are created
}