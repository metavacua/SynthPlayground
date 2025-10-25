import json
import os
import re
from collections import Counter
from datetime import datetime


def analyze_protocol_completeness(used_tools, protocol_tools):
    """
    Analyzes the completeness of the protocols by comparing used tools to protocol tools.
    """
    unreferenced = sorted(list(set(used_tools) - protocol_tools))
    unused = sorted(list(protocol_tools - set(used_tools)))
    return unreferenced, unused


def analyze_tool_centrality(used_tools):
    """
    Analyzes the centrality of tools by counting their usage.
    """
    if not used_tools:
        return []
    return Counter(used_tools).most_common()


def analyze_plan_registry(registry, root_dir):
    """
    Analyzes the plan registry for dead links.
    """
    dead_links = []
    for name, path in registry.items():
        if not os.path.exists(os.path.join(root_dir, path)):
            dead_links.append((name, path))
    return dead_links


def analyze_documentation(system_docs_content):
    """
    Analyzes the system documentation for missing docstrings.
    """
    pattern = re.compile(r"### `(.*?\.py)`\n\n_No module-level docstring found._")
    return pattern.findall(system_docs_content)


def analyze_system_health(log_content, postmortem_dir, session_start_time_iso):
    """
    Analyzes the system health for "absence of evidence" anomalies.
    """
    report_parts = []
    issues_found = False

    try:
        session_start_time = datetime.fromisoformat(session_start_time_iso)
    except ValueError:
        report_parts.append(
            f"❌ **Invalid Session Start Time:** Could not parse '{session_start_time_iso}'."
        )
        return "\n".join(report_parts)

    # 1. Log Staleness Check
    if not log_content:
        report_parts.append(
            "❌ **Log Staleness Detected:** Log content is empty. The agent's logging system may be broken."
        )
        issues_found = True
    else:
        try:
            last_log = json.loads(log_content[-1])
            last_timestamp_str = last_log.get("timestamp")
            if not last_timestamp_str:
                raise KeyError("Timestamp not found in last log entry")

            # Make timestamps timezone-aware for comparison if they aren't already
            last_timestamp = datetime.fromisoformat(last_timestamp_str)
            if last_timestamp.tzinfo is None:
                last_timestamp = last_timestamp.replace(tzinfo=datetime.timezone.utc)
            if session_start_time.tzinfo is None:
                session_start_time = session_start_time.replace(
                    tzinfo=datetime.timezone.utc
                )

            if last_timestamp < session_start_time:
                report_parts.append(
                    f"❌ **Log Staleness Detected:** The last log entry was at {last_timestamp.isoformat()}, which is before the current session started at {session_start_time_iso}. The logging system may be broken or stalled."
                )
                issues_found = True
        except (IndexError, json.JSONDecodeError, KeyError) as e:
            report_parts.append(
                f"❌ **Log Staleness Detected:** Could not parse the last log entry. The log file may be corrupted. Error: {e}"
            )
            issues_found = True

    # 2. Success-Only Task Check
    tasks = {}
    for line in log_content:
        try:
            log_entry = json.loads(line)
            log_time_str = log_entry.get("timestamp")
            if not log_time_str:
                continue

            log_time = datetime.fromisoformat(log_time_str)
            if log_time.tzinfo is None:
                log_time = log_time.replace(tzinfo=datetime.timezone.utc)

            # Only consider logs from the current session
            if log_time < session_start_time:
                continue

            task_id = log_entry.get("task_id", "unknown_task")
            if task_id not in tasks:
                tasks[task_id] = {"actions": 0, "failures": 0}
            tasks[task_id]["actions"] += 1
            if log_entry.get("outcome", {}).get("status") == "FAILURE":
                tasks[task_id]["failures"] += 1
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    suspicious_tasks = []
    ACTION_THRESHOLD = 5
    for task_id, data in tasks.items():
        if data["actions"] > ACTION_THRESHOLD and data["failures"] == 0:
            suspicious_tasks.append(task_id)

    if suspicious_tasks:
        report_parts.append(
            "⚠️ **Success-Only Task Logs:** The following tasks had a high number of actions but no failures since the session started, which may indicate that failures were not logged:"
        )
        for task_id in suspicious_tasks:
            report_parts.append(f"  - `{task_id}`")
        issues_found = True

    # 3. Incomplete Post-Mortem Check
    recent_failures = []
    for line in log_content:
        try:
            log_entry = json.loads(line)
            log_time_str = log_entry.get("timestamp")
            if not log_time_str:
                continue

            log_time = datetime.fromisoformat(log_time_str)
            if log_time.tzinfo is None:
                log_time = log_time.replace(tzinfo=datetime.timezone.utc)

            if (
                log_time >= session_start_time
                and log_entry.get("outcome", {}).get("status") == "FAILURE"
                and log_entry.get("task_id")
            ):
                recent_failures.append(log_entry["task_id"])
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

    incomplete_postmortems = []
    for task_id in set(recent_failures):
        found_pm = False
        if os.path.exists(postmortem_dir):
            for filename in os.listdir(postmortem_dir):
                if task_id in filename and filename.endswith(".md"):
                    filepath = os.path.join(postmortem_dir, filename)
                    if os.path.getsize(filepath) > 0:
                        found_pm = True
                        break
        if not found_pm:
            incomplete_postmortems.append(task_id)

    if incomplete_postmortems:
        report_parts.append(
            "❌ **Incomplete Post-Mortems Detected:** The following tasks failed during this session but do not have a corresponding, non-empty post-mortem report:"
        )
        for task_id in incomplete_postmortems:
            report_parts.append(f"  - `{task_id}`")
        issues_found = True

    if not issues_found:
        report_parts.append("✅ **No new critical or warning level issues found.**")

    return "\n".join(report_parts)
