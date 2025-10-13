# Meta-Protocol: Enforced Prohibition

This protocol establishes a critical link between the definition of a prohibition and its automated enforcement. It is designed to prevent a critical process gap where a protocol may forbid an action, but no technical mechanism exists to enforce that prohibition.

## The Problem: Unenforced Prohibitions

A protocol can state that a tool like `reset_all` is forbidden, but if the core execution engine (e.g., `master_control.py`) does not have explicit logic to block the use of that tool, the prohibition is merely a suggestion. It relies on the agent's correct interpretation and adherence, which can fail. This creates a severe safety and reliability risk.

## The Solution: Mandated Technical Enforcement

This protocol closes that gap by mandating that any protocol rule that **prohibits** a specific, identifiable action (like using a tool or calling a function) **must** be accompanied by a corresponding automated enforcement mechanism in the system's codebase.

**Rule `enforced-prohibition-link`**: For any protocol rule that includes the words "prohibit," "forbid," or "disallow" in its description, a corresponding technical control must be implemented to enforce it. The protocol definition should cite the tool or module responsible for this enforcement.