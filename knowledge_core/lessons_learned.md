# Lessons Learned

This document is a repository for accumulating knowledge and insights gained from previous tasks. It serves as a reference to avoid repeating past mistakes and to leverage successful strategies in future work.

---
**Task ID:** [meta-analysis-20251007]
**Date:** 2025-10-07
**Observation:** During an analysis task, I identified a tool (`fdc_cli.py`) that was not directly called by my most recent protocol implementation. I concluded it was obsolete and planned to delete it.
**Insight (Faulty Reasoning):** My reasoning was flawed because it was based on an incomplete understanding. I equated "not immediately used by my current implementation" with "useless." I failed to consider the historical context or the deeper purpose of the tool, which was to enforce formal properties on development plans.
**Actionable Guidance:** Assume repository artifacts have a purpose until proven otherwise through rigorous investigation. Absence of immediate understanding is not evidence of obsolescence. Before proposing the deletion of any component, I must first perform a thorough analysis of its intended function, its history, and the principles it represents.
---