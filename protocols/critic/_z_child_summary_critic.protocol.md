# --- Child Module: `critic` ---

# Protocol: Critic `reset_all` Prohibition

This protocol establishes a critical safeguard to protect the integrity of the development workflow.

## Rule: `critic-no-reset`

The agent assigned the role of 'Code Review Critic' is explicitly and strictly forbidden from using the `reset_all` tool.

**Rationale:** The `reset_all` tool is a destructive action that reverts all changes in the workspace. Its use by a review agent could lead to the accidental deletion of work-in-progress, creating a significant disruption. This protocol ensures that the critic's function is limited to analysis and feedback, preventing it from taking destructive actions.

This prohibition is non-negotiable and must be adhered to by any agent assuming the 'Code Review Critic' role.

**Enforcement Mechanism:** The Code Review Critic is not implemented in this repository. Its behavior is governed by the compiled `AGENTS.md` file, which is consumed by an external orchestration system. The inclusion of this protocol in `AGENTS.md` constitutes the complete implementation of this safeguard from the perspective of this codebase.

---
