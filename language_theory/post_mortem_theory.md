# A Theory of Post-Mortems in Software Engineering

## 1. Core Philosophy: Learning from Failure

The fundamental purpose of a post-mortem is not to assign blame, but to **learn from failure** and improve the resilience of the system. Every incident, from a minor glitch to a catastrophic outage, is an unplanned investment in the education of the organization. The goal is to maximize the return on that investment.

A successful post-mortem culture is built on the following principles:

-   **Blamelessness:** The analysis must focus on systemic and process-related causes, not on individual errors. It assumes that everyone involved acted with good intentions based on the information they had at the time. You cannot "fix" people, but you can fix the systems and processes that support them.
-   **Constructive Focus:** The tone should be forward-looking and constructive. The objective is to identify opportunities for improvement, not to vent frustration.
-   **Shared Ownership:** Incidents are a collective responsibility. The post-mortem process should be collaborative, involving individuals from different teams and perspectives to build a complete picture.

## 2. When to Write a Post-Mortem

A post-mortem should be triggered by any significant, undesirable event. It is crucial to define these triggers objectively *before* an incident occurs. Common triggers include:

-   Any user-visible downtime or service degradation.
-   Data loss or corruption of any kind.
-   Any incident requiring manual intervention from an on-call engineer (e.g., emergency rollback, traffic rerouting).
-   A time-to-resolution that exceeds a predefined threshold.
-   A failure in monitoring or alerting that resulted in manual discovery of the incident.
-   At the request of any stakeholder who believes a deeper analysis is warranted.

## 3. Anatomy of an Effective Post-Mortem

A high-quality post-mortem document is a structured record designed for clarity, analysis, and action. It should contain the following sections:

-   **Executive Summary:** A brief, one-paragraph overview of the incident, its impact, the duration, and the key outcome of the analysis. This is for readers who need to understand the event at a high level.
-   **Impact Assessment:** A detailed and quantitative description of the impact on users, systems, and the business. This should include metrics like the number of affected users, the duration of the impact, and any financial or reputational costs.
-   **Timeline of Events:** A detailed, chronological log of events from the initial trigger to the final resolution. This should include automated alerts, key actions taken by responders, and important communications. This timeline is the factual backbone of the analysis.
-   **Root Cause Analysis (RCA):** A deep investigation into the contributing factors. This should go beyond the immediate trigger (e.g., "a bad code push") to uncover the underlying systemic weaknesses (e.g., "the testing environment doesn't accurately model a production data race condition, and the deployment process lacks a phased rollout stage"). A "Five Whys" or similar technique is often effective here.
-   **Corrective and Preventive Actions:** A list of specific, measurable, achievable, relevant, and time-bound (SMART) action items. Each item must have a clear owner and a priority level. These are the concrete steps that will be taken to prevent recurrence.
-   **Lessons Learned:** A higher-level summary of the knowledge gained. What did we learn about our system, our processes, or our assumptions that we didn't know before?

## 4. The Post-Mortem Process and Culture

The process surrounding the document is as important as the document itself.

1.  **Collaboration and Data Gathering:** The post-mortem should be a collaborative document (e.g., a shared Google Doc or wiki page) where all involved parties can contribute to the timeline and analysis in real-time.
2.  **Review:** Once a draft is complete, it should be reviewed by a group of senior engineers or a dedicated post-mortem review committee. This ensures the root cause analysis is sufficiently deep and the action items are meaningful.
3.  **Knowledge Sharing:** The final post-mortem must be shared widely. It should be stored in a central, searchable repository. Consider "Post-Mortem of the Month" newsletters, reading clubs, or presentations to disseminate the lessons learned to the entire engineering organization.
4.  **Tracking Action Items:** The process does not end when the document is published. There must be a reliable system for tracking the implementation of corrective actions. Uncompleted action items are a sign of a failing post-mortem culture.
5.  **Rewarding Participation:** Publicly recognize and reward individuals for excellent incident response and high-quality post-mortem analysis. This reinforces the idea that learning from failure is a valued engineering practice.