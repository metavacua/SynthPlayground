"""
A tool for performing temporal orientation by fetching a summary of a concept from DBPedia.
"""

import sys
from dbpedia_client import get_abstract


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 temporal_orienter.py <concept>")
        sys.exit(1)

    concept = sys.argv[1]
    summary = get_abstract(concept)

    if summary:
        print(summary)
    else:
        print(f"No summary found for '{concept}'")


if __name__ == "__main__":
    main()
