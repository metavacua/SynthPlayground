# Git Hook Setup for Automatic Protocol Synchronization

This guide explains how to set up a `post-merge` Git hook. This hook will automatically run `make build-protocol` every time you pull or merge changes from the remote repository. This ensures that your local `AGENTS.md` file is always up-to-date with the canonical version built from `protocol_sources/`.

This is a critical step to ensure a consistent development environment for both you and the AI agent, Jules.

## Instructions

Follow these steps in your terminal, from the root of the `SynthPlayground` repository.

### 1. Navigate to the Git Hooks Directory

The hooks for a Git repository are located in the `.git/hooks/` directory.

```bash
cd .git/hooks
```

### 2. Create the `post-merge` Hook File

Create a new file named `post-merge`.

```bash
touch post-merge
```

### 3. Make the Hook Executable

The script needs to have execute permissions to run.

```bash
chmod +x post-merge
```

### 4. Add the Script Content

Open the `post-merge` file in your favorite text editor and add the following script content. This script will run the `make build-protocol` command from the root of the repository.

```bash
#!/bin/sh
#
# This hook runs after a successful merge.
# It automatically rebuilds the AGENTS.md file to ensure it stays in sync.

echo "Running post-merge hook to rebuild AGENTS.md..."
make build-protocol
echo "Hook finished."

exit 0
```

### 5. Return to the Repository Root

Navigate back to the root directory of the repository.

```bash
cd ../..
```

That's it! Now, every time you successfully run `git pull` or `git merge`, the hook will automatically execute, and your `AGENTS.md` will be rebuilt. This guarantees that you are always working with the latest version of the agent protocol.