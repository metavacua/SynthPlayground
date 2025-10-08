# Local Integration Guide: Closing the Triangle with Git Hooks

## 1. Objective

This guide explains how to set up a `pre-push` Git hook on your local machine. The purpose of this hook is to "close the triangle" between your local development environment, the GitHub repository, and Jules's operational environment.

By triggering the `update-knowledge-core.yml` workflow *before* you push, you are proactively updating the repository's Knowledge Core with the context of your latest changes. This allows Jules to be aware of your work in near real-time, enabling a much smoother and more intelligent collaboration.

## 2. Prerequisites

You must have the **GitHub CLI** installed on your local machine. It is a free, official tool that allows you to interact with GitHub from your terminal.

-   **Installation Instructions:** [https://cli.github.com/](https://cli.github.com/)
-   **Authentication:** Once installed, run `gh auth login` to authenticate with your GitHub account.

## 3. Step-by-Step Setup

Follow these instructions in your local terminal from the root of the `SynthPlayground` repository.

### Step 3.1: Navigate to the Hooks Directory

The `.git` directory in your repository contains a `hooks` folder for local scripts.

```bash
cd .git/hooks
```

### Step 3.2: Create the `pre-push` Hook File

Create a new file named `pre-push`.

```bash
touch pre-push
```

### Step 3.3: Add the Hook Script

Open the `pre-push` file in your favorite text editor and paste the following script into it.

```sh
#!/bin/sh

# Get the name of the remote and the branch being pushed to.
remote="$1"
url="$2"

# Read the details of what is being pushed.
while read local_ref local_sha remote_ref remote_sha
do
    # Check if the push is targeting the 'main' branch.
    # We only want to trigger the workflow for pushes to main.
    if [ "$remote_ref" = "refs/heads/main" ]; then
        echo "PRE-PUSH HOOK: Push to 'main' branch detected."
        echo "Triggering 'Update Knowledge Core' workflow..."

        # Use the GitHub CLI to trigger the workflow on the current branch.
        # This makes the latest commit from your local branch available to the workflow.
        gh workflow run update-knowledge-core.yml --ref "$(git rev-parse --abbrev-ref HEAD)"

        echo "PRE-PUSH HOOK: Workflow triggered successfully. Proceeding with push."
    fi
done

exit 0
```

### Step 3.4: Make the Hook Executable

You must give the `pre-push` script execute permissions.

```bash
chmod +x pre-push
```

## 4. How It Works

You're all set! Now, whenever you run `git push` to the `main` branch, this `pre-push` hook will automatically execute.

1.  It checks that you are pushing to `main`.
2.  It uses the GitHub CLI (`gh`) to send a `workflow_dispatch` event to the `update-knowledge-core.yml` workflow.
3.  Crucially, it tells the workflow to run using the code from your *current local branch* (`--ref "$(git rev-parse --abbrev-ref HEAD)"`).
4.  The workflow then runs in GitHub Actions, checking out your latest commit, and executing the `dependency_graph_generator.py` and `symbol_map_generator.py` scripts.
5.  The updated `dependency_graph.json` and `symbols.json` are committed back to your branch by the workflow.

This process ensures that the Knowledge Core artifacts are always in sync with the very latest code, providing a seamless, automated, and powerful foundation for our development partnership.