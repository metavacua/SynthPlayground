## 5. Manual Protocol Rebuild Procedure

This section defines the protocol for manually rebuilding `AGENTS.md` within an active session. This procedure is mandatory whenever the agent modifies any file within the `protocol_sources/` directory.

### Agent Directives:

1.  **Declare Intent:** After successfully modifying a file in `protocol_sources/`, you must clearly state your intention to rebuild the `AGENTS.md` file.

2.  **Request User Approval:** You must ask for explicit permission from the user before proceeding with the rebuild. Use the `request_user_input` tool for this purpose. The request must clearly state that you intend to run `make build-protocol`.

3.  **Await Approval:** Do not proceed until the user has explicitly approved the action.

4.  **Execute Rebuild:** Upon receiving user approval, execute the build command using the `run_in_bash_session` tool:
    ```bash
    make build-protocol
    ```

5.  **Verify Build:** After execution, you must read the `AGENTS.md` file to confirm that the changes have been successfully incorporated.

This protocol ensures that the user maintains full control over any changes to the agent's core operating instructions that are initiated by the agent itself.