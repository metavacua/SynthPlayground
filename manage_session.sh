#!/bin/bash

set -e

# This script manages the AGENTS.md file for an agent session.

# --- Configuration ---
ROOT_DIR=$(git rev-parse --show-toplevel)
AGENTS_MD_FILE="$ROOT_DIR/AGENTS.md"
TEMP_AGENTS_MD_FILE=$(mktemp)

# --- Functions ---

# Builds AGENTS.md into a temporary file and then atomically moves it into place.
setup() {
    echo "Building AGENTS.md..."
    python3 "$ROOT_DIR/tooling/builder.py" --target agents-md -- --output-file "$TEMP_AGENTS_MD_FILE"

    echo "Atomically updating AGENTS.md..."
    mv "$TEMP_AGENTS_MD_FILE" "$AGENTS_MD_FILE"

    echo "AGENTS.md is ready for the session."
}

# Removes the AGENTS.md file.
cleanup() {
    echo "Cleaning up AGENTS.md..."
    if [ -f "$AGENTS_MD_FILE" ]; then
        rm "$AGENTS_MD_FILE"
        echo "AGENTS.md removed."
    else
        echo "AGENTS.md not found, nothing to clean up."
    fi
}

# --- Main Logic ---
main() {
    if [ "$1" == "setup" ]; then
        setup
    elif [ "$1" == "cleanup" ]; then
        cleanup
    else
        echo "Usage: $0 {setup|cleanup}"
        exit 1
    fi
}

main "$@"