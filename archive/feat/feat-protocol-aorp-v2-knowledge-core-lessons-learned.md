# Lessons Learned

This document records lessons learned during the agent's operation. It is intended to be a cumulative record of insights that can inform future planning and execution.

## 2025-10-06: Protocol Implementation vs. Documentation

**Lesson:** Documenting a protocol is insufficient; it must be implemented and enforced through code to be effective. A protocol described only in Markdown is a description of a desired state, not a functional system.

**Triggering Event:** A code review for the AORP v2.0 implementation failed because only the documentation (`AGENTS.md`) was updated, without any of the underlying code to execute the orientation cascade.

**Resolution:** The plan was revised to create a tangible `make orient` target, which provides an executable entry point for the protocol. This makes the protocol verifiable and enforceable, not just descriptive.