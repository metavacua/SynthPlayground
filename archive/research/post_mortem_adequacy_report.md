# Post-Mortem Tooling: Adequacy and Improvement Report

**Date:** 2025-10-15
**Author:** Jules
**Status:** Complete

## 1. Introduction

This report assesses the adequacy of the post-mortem tooling and processes within this repository. The evaluation is based on a synthesized theory of modern, blameless post-mortems derived from established industry best practices (see `language_theory/post_mortem_theory.md`). The goal of this analysis is to identify strengths, weaknesses, and actionable opportunities for improvement.

## 2. Summary of Post-Mortem Theory

An effective post-mortem system is a cornerstone of a resilient engineering culture. It is not a tool for assigning blame, but a process for learning from failure. The core principles are:

-   **Blamelessness:** Focus on systems and processes, not individuals.
-   **Deep Analysis:** Go beyond immediate triggers to uncover true root causes.
-   **Actionable Outcomes:** Produce concrete, trackable actions to prevent recurrence.
-   **Knowledge Sharing:** Ensure lessons are disseminated effectively throughout the organization.

A mature post-mortem process transforms incidents from liabilities into investments in organizational knowledge and system robustness.

## 3. Analysis of Existing Tooling

The repository contains a mix of post-mortem artifacts that represent different levels of maturity.

### 3.1. `postmortem.md` (Basic Template)

-   **Description:** A simple, markdown-based template for basic incident reporting.
-   **Strengths:**
    -   Easy to use and understand.
    -   Covers the bare essentials (summary, what went well/wrong, lessons).
-   **Weaknesses:**
    -   Lacks structure for deep analysis.
    -   "Lessons Learned" are free-form text, making them difficult to track or automate.
    -   Does not enforce a blameless or root-cause-oriented approach.
-   **Adequacy:** **Low.** This template is suitable only for the most minor incidents or for organizations just beginning to adopt a post-mortem culture.

### 3.2. `postmortem_catastrophic_failure.md` (Example Report)

-   **Description:** A detailed, well-written report analyzing a severe process failure.
-   **Strengths:**
    -   Excellent example of a blameless, in-depth root cause analysis.
    -   Clearly separates timeline, root causes, and lessons.
    -   Proposes specific, actionable changes to protocols and tooling.
-   **Weaknesses:**
    -   It is a one-off report, not a reusable template. Its quality is dependent on the diligence of the author.
-   **Adequacy:** **High (as an example).** This report serves as an excellent model for what a good post-mortem should be.

### 3.3. `postmortems/structured_postmortem.md` (Advanced Template)

-   **Description:** A sophisticated, data-driven template for structured analysis and lesson generation.
-   **Strengths:**
    -   **Highly Structured:** Enforces a rigorous analytical process (Objective vs. Outcome, Causal Analysis).
    -   **Data-Driven:** Demands log evidence to support claims.
    -   **Machine-Readable Lessons:** The core innovation. It generates lessons as JSON objects with categories, severity, and specific, actionable changes. This is a critical step toward automating the self-improvement loop.
-   **Weaknesses:**
    -   The JSON lesson format, while powerful, could be complex for users to fill out correctly.
    -   It is currently located in a subdirectory and not established as the default, likely leading to inconsistent adoption.
-   **Adequacy:** **High.** This template represents a state-of-the-art approach to post-mortems, aligning perfectly with the goal of turning analysis into automated, systemic improvement.

## 4. Recommendations

The repository has excellent but fragmented tooling. The primary goal should be to standardize on the most advanced template and deprecate the simpler one.

1.  **Standardize on the Structured Template:** The `postmortems/structured_postmortem.md` should be moved to the root of the repository and renamed `postmortem.md`. The original, simpler `postmortem.md` should be archived or deleted. This makes the best-practice template the default and easiest path for all users.
2.  **Incorporate Best Practices from the Catastrophic Failure Report:** The `structured_postmortem.md` template should be enhanced to include an explicit "Impact Assessment" section and a more detailed "Timeline of Events" section, as demonstrated in the `postmortem_catastrophic_failure.md` report. This combines the structured, machine-readable format with the narrative clarity needed for human readers.
3.  **Develop a "Lesson Consumer" Tool:** The existence of a structured lesson format implies the need for a tool that consumes these lessons. A follow-up project should be created to build a `lesson_consumer.py` script that can parse the JSON output from post-mortems and, where possible, automatically apply the proposed changes (e.g., updating protocol files).

By implementing these changes, the repository can move from a passive documentation culture to an active, automated self-improvement ecosystem, maximizing the value gained from every operational incident.