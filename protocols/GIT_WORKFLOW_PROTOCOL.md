# Git Workflow Protocol

**Note:** This file is for human documentation purposes only and is not intended for use in machine-readable toolchains.

## 1. Introduction

This document defines the standard operating procedure for all git-related activities within this environment. Due to specific environmental constraints, a non-standard workflow is required to ensure stability and predictability. Adherence to this protocol is mandatory for all tasks involving code changes.

The primary limitations discovered are:
- Direct `git commit` operations do not behave as expected and should not be used.
- `git merge` is unsupported as a consequence of the commit limitations.
- The `submit` tool is the sole method for finalizing and proposing changes.

## 2. Core Principles

- **Atomic Changes:** Treat every task as a single, atomic set of changes. Do not attempt to build a complex commit history.
- **Submission via Tooling:** All changes must be proposed using the `submit` tool. Direct `git push` or `git commit` commands are forbidden.
- **Branch for Isolation:** Use local branches purely for isolating work-in-progress. This allows for easy cleanup and context switching.

## 3. Naming Conventions

- **Branch Names:** Branch names should be descriptive and use kebab-case (e.g., `add-user-authentication`, `fix-login-bug`).
- **Commit Messages:** Commit messages should follow the Conventional Commits specification (e.g., `feat: add user authentication`, `fix: resolve login bug`).

## 4. Standard Workflow

Follow these steps for every development task.

### Step 1: Task Initialization & Planning

1.  **Understand the Goal:** Thoroughly analyze the user's request and any provided resources.
2.  **Explore the Codebase:** Use `list_files`, `read_file`, and `grep` to understand the relevant parts of the repository.
3.  **Create a Plan:** Formulate a detailed, step-by-step plan. Set the plan using the `set_plan` tool.
4.  **Create an Isolation Branch:** Before making any changes, create a new local branch. This prevents accidental modifications to `main`.

### Step 2: Development & Verification

1.  **Modify Files:** Use the provided file system tools (`create_file_with_block`, `replace_with_git_merge_diff`, `delete_file`) to implement the planned changes.
2.  **Verify Every Change:** After every modification, use a read-only tool (`read_file`, `list_files`) to confirm the change was applied correctly. **Do not proceed until the change is verified.**
3.  **Check Status:** Use `git status` to check the status of your changes.
4.  **Stage Changes:** Use `git add <file>` to stage your changes for submission.
5.  **Test Continuously:** Run relevant tests frequently using the `make test` command or other testing scripts to ensure changes are correct and do not introduce regressions.

### Step 3: Pre-Submission Finalization

Before submitting, it is highly recommended to run the automated pre-submission check. This tool will lint your code and run tests to catch common issues before you request a formal review.

After the pre-submission check passes (or if you are intentionally skipping it for a valid reason), execute the following manual pre-commit steps by calling `pre_commit_instructions()` and following the output. This is a summary of the expected steps:

1.  **Run Final Tests:** Execute the entire test suite to catch any final issues. Address any failures that are within the scope of the task.
2.  **Frontend Verification (If Applicable):** If the changes affect any UI, use the `frontend_verification_instructions` tool to generate and submit a visual verification.
3.  **Request Code Review:** Call `request_code_review` to get feedback on your changes.
4.  **Address Feedback:** Carefully review the feedback and make any necessary corrections.
5.  **Record Learnings:** Call `initiate_memory_recording` to document key takeaways from the task.

### Step 4: Submission

1.  **Submit Changes:** Use the `submit` tool to propose your changes.
    -   `branch_name`: Use the same descriptive branch name from Step 1.
    -   `commit_message`: Write a clear, concise commit message explaining the "what" and "why" of the change.
    -   `title`: A short, descriptive title for the submission.
    -   `description`: A more detailed explanation of the changes.

## 5. Handling Issues

- **Reverting a File:** If a file modification is incorrect, restore it to its original state using `restore_file <filepath>`.
- **Abandoning Changes:** To discard all current changes, switch back to the `main` branch and delete your feature branch.
- **Handling Code Review Feedback:** If you receive feedback on your changes, you can update your branch by checking it out and making the necessary changes. Once you are done, you can submit the updated branch again.
- **Rebasing:** To update your feature branch with the latest changes from the `main` branch, you can rebase it.
- **Squashing Commits:** To combine multiple commits into a single commit, you can use interactive rebase.
