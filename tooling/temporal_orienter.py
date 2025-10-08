import argparse
import datetime
import os

# Define the path to the temporal orientation log file.
LOG_FILE_PATH = os.path.join("knowledge_core", "temporal_orientation.md")


def log_orientation_entry(summary_text):
    """
    Appends a timestamped research summary to the temporal orientation log.

    Args:
        summary_text (str): The summary of research findings provided by the agent.
    """
    # Get the current timestamp in a clean, readable UTC format.
    timestamp = datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    # Format the entry in a structured markdown format for clarity and consistency.
    log_entry = f"\n## Entry: {timestamp}\n\n{summary_text}\n\n---\n"

    # Append the new entry to the log file.
    try:
        with open(LOG_FILE_PATH, "a", encoding="utf-8") as f:
            f.write(log_entry)
        print(f"Successfully appended research summary to {LOG_FILE_PATH}")
    except FileNotFoundError:
        print(f"Error: Log file not found at {LOG_FILE_PATH}.")
        print("Please ensure the knowledge_core has been initialized correctly.")
        # The protocol assumes the file exists from Phase 0. This tool should not create it.


def main():
    """
    Main function to parse the command-line arguments and run the logger.
    """
    parser = argparse.ArgumentParser(
        description="A tool to log timestamped research findings to the temporal "
        "orientation file."
    )
    parser.add_argument(
        "summary",
        type=str,
        help="A quote-enclosed summary of the research findings to be logged.",
    )
    args = parser.parse_args()

    if not args.summary.strip():
        print("Error: Summary cannot be empty.")
        return

    log_orientation_entry(args.summary)


if __name__ == "__main__":
    main()
