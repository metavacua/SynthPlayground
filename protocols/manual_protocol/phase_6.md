# Phase 6

Post-Mortem & Knowledge Update (Self-Improvement Loop)
Post-Mortem Analysis: Upon task completion (success or failure), perform a post-mortem. Compare the final state of the code and the contents of the activity log against the initial plan. Identify deviations, errors, and inefficiencies.

Generate Report: Summarize your findings in a postmortem.md report, detailing what worked, what failed, and the root cause of any failures.

Meta-RAG for Cross-Task Learning: Before beginning a new task (during Phase 2), perform a RAG query against the logs/ directory. Search for log entries and postmortem.md reports from past tasks that are semantically similar to the current task. Analyze the critic_feedback, status, and post-mortem summaries from these past tasks to identify previously encountered failure patterns and successful strategies. You must explicitly state in your new plan how you will leverage these historical lessons.