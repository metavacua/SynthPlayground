# Lessons Learned

This document records lessons learned during the agent's operation. It is intended to be a cumulative record of insights that can inform future planning and execution.

## 2025-10-06: Protocol Implementation vs. Documentation

**Lesson:** Documenting a protocol is insufficient; it must be implemented and enforced through code to be effective. A protocol described only in Markdown is a description of a desired state, not a functional system.

**Triggering Event:** A code review for the AORP v2.0 implementation failed because only the documentation (`AGENTS.md`) was updated, without any of the underlying code to execute the orientation cascade.

**Resolution:** The plan was revised to create a tangible `make orient` target, which provides an executable entry point for the protocol. This makes the protocol verifiable and enforceable, not just descriptive.

## 2025-10-08: Tooling vs. Integration

**Lesson:** Creating a tool that *enables* a protocol is not the same as *integrating* that protocol into the core operational loop. The agent's own behavior must be modified to *use* the new tooling as a mandatory, non-negotiable step.

**Triggering Event:** A code review for the AORP v2.0 implementation failed for a second time. While the `fdc_cli.py start` command existed, I (the agent) did not programmatically call it upon receiving a new task. The protocol was available but not integrated into my own decision-making process.

**Resolution:** The `AGENTS.md` protocol was updated with a new "Meta-Protocol" section containing a direct, first-person standing order. This order explicitly binds my own core loop to execute the `fdc_cli.py start` command as the first action for any new task, making the integration explicit and enforceable.