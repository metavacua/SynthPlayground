## 4. Core Tooling
The Master Control Graph orchestrates a suite of tools to perform its functions:
- **`tooling/research.py`:** Contains the `execute_research_protocol` function, the unified tool for all information gathering.
- **`tooling/research_planner.py`:** Contains the `plan_deep_research` function for L4 tasks.
- **`tooling/environmental_probe.py`:** Used by the `ORIENTING` state to assess the VM's capabilities.

This FSM-based architecture ensures that the protocol is not just a document, but the running code that governs my every action, making my development process transparent, robust, and reliable.