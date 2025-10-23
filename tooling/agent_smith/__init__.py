"""
This package, named 'Agent Smith', is a toolset designed for metamorphic
testing of the agent's core protocol compilation system.

It works by creating isolated sandbox environments, introducing mutations
(e.g., deleting a protocol file), running the protocol compiler, and verifying
that the resulting `AGENTS.md` artifact reflects the mutation as expected.
This allows for robust testing of the hierarchical compiler's resilience and
correctness.
"""
