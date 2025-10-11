#!/bin/bash

set -e # Exit on error.

if [ -z "$1" ]; then
  echo "Usage: $0 <branch_name>"
  exit 1
fi

branch="$1"

# Ensure archive directories exist.
mkdir -p agents_archive
mkdir -p agents_references_archive

echo "Processing branch: $branch"
sanitized_branch_name=$(echo "$branch" | tr '/' '_')

# Use git ls-tree to find AGENTS.md/agent.md files in the branch.
git ls-tree -r --name-only "origin/$branch" | grep -E 'AGENTS\.md$|agent\.md$' | while read -r filepath; do
  echo "Found agent file: $filepath in branch $branch"
  # Create a unique name for the archived file.
  sanitized_filepath=$(echo "$filepath" | tr '/' '_')
  output_filename="agents_archive/${sanitized_branch_name}_${sanitized_filepath}"
  # Get the file content from git and save it.
  git show "origin/$branch:$filepath" > "$output_filename"
  echo "  -> Archived to $output_filename"
done

# Use git grep to find files that reference "AGENTS.md" or "agent.md".
# We'll do this in two passes to avoid duplicating files.

# Pass 1: Find files with "AGENTS.md"
git grep -l "AGENTS.md" "origin/$branch" -- . ':(exclude)agents_archive/*' ':(exclude)agents_references_archive/*' | sed "s|origin/$branch:||" | while read -r filepath; do
  echo "Found reference to AGENTS.md in: $filepath in branch $branch"
  sanitized_filepath=$(echo "$filepath" | tr '/' '_')
  output_filename="agents_references_archive/${sanitized_branch_name}_${sanitized_filepath}"
  git show "origin/$branch:$filepath" > "$output_filename"
  echo "  -> Archived to $output_filename"
done

# Pass 2: Find files with "agent.md" that we haven't already archived.
git grep -l "agent.md" "origin/$branch" -- . ':(exclude)agents_archive/*' ':(exclude)agents_references_archive/*' | sed "s|origin/$branch:||" | while read -r filepath; do
  sanitized_filepath=$(echo "$filepath" | tr '/' '_')
  output_filename="agents_references_archive/${sanitized_branch_name}_${sanitized_filepath}"
  if [ ! -f "$output_filename" ]; then
    echo "Found reference to agent.md in: $filepath in branch $branch"
    git show "origin/$branch:$filepath" > "$output_filename"
    echo "  -> Archived to $output_filename"
  fi
done

echo "Archival process for branch $branch complete."