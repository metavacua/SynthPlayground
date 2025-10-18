# --- Child Module: `critic` ---

# Protocol: Critic `reset_all` Prohibition

This protocol establishes a critical safeguard to protect the integrity of the development workflow.

## Rule: `critic-no-reset`

The agent assigned the role of 'Code Review Critic' is explicitly and strictly forbidden from using the `reset_all` tool.

**Rationale:** The `reset_all` tool is a destructive action that reverts all changes in the workspace. Its use by a review agent could lead to the accidental deletion of work-in-progress. This protocol ensures that the critic's function is limited to analysis and feedback. This prohibition is non-negotiable.

**Enforcement Mechanism:** This protocol is enforced by an external orchestration system that consumes the compiled `AGENTS.md` file.

---