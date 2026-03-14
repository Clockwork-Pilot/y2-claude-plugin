# Claude Code Plugin

A minimal Claude plugin written in Python that implements hook handlers and logs all hook invocations.

## Submodules

This project includes the following Git submodules:

- **y2_pycov** - Python coverage utilities (https://github.com/YuraLitvinov/y2-pycov)
- **knowledge_tool** - Knowledge tool system (https://github.com/YaroslavLitvinov/y2-knowledge-tool)

To clone with submodules:
```bash
git clone --recurse-submodules <repository-url>
```

To update submodules after cloning:
```bash
git submodule update --init --recursive
```

## Run in docker
Use docker image from this repo: github.com:YuraLitvinov/y2-docker-claude
Build & Run docker container as specified in their readme.

```
touch $(pwd)/.claude.local.json && \
mkdir $(pwd)/.credentials -p && \
  docker run -it --rm  \
    --user 1000:1000  \
    -w /project \
    -v $HOME/.ssh/id_ed25519.pub:/home/node/.ssh/id_ed25519.pub:ro \
    -v $SSH_AUTH_SOCK:/ssh-agent \
    -e SSH_AUTH_SOCK=/ssh-agent \
    -v $(pwd)/.credentials:/home/node/.claude:Z \
    -v $(pwd)/.claude.local.json:/home/node/.claude.json:Z \
    -v $(pwd):/project y2-coder

# Use forwarded SSH Key Inside of container
ssh-add -l
# ssh-add ~/.ssh/id_ed25519

# test signature
echo "test" | ssh-keygen -Y sign     -f ~/.ssh/id_ed25519     -n file

# Set github signing key
git config --global user.name  "Yaroslav Litvinov"
git config --global user.email "yaroslav.litvinov@gmail.com"
git config --global user.signingkey ~/.ssh/id_ed25519.pub
git config --global gpg.format ssh
git config --global commit.gpgsign true
git config --global --list

# Inside of container - init specify for project
specify init --here --ai claude

# Inside of container - run claude
source .venv/bin/activate && claude --model claude-haiku-4-5 --plugin-dir /project
```

## Workflow
1. Run Claude with --worktree option so it makes changes in separate worktree, in folder .claude/worktrees/
2. Commit changes in worktree
3. Run `git rebase worktree-test` to apply changes from worktree to main branch (Resolve conflicts if any)
4. `git worktree remove .claude/worktrees/test` - remove worktree
5. `git worktree list` - list all worktrees
6. `git branch -d worktree-test` - remove branch
7. `git branch` - list all branches

## Features

- Logs all hook events to `hooks.log`
- Returns exit code 0 to allow Claude Code to proceed
- Separate handler configuration for each hook type
- Uses absolute paths for both interpreter and handlers

## Core Tools

### Knowledge Base Tool
API-first knowledge base system using JSON Patch operations (RFC 6902) with automatic markdown rendering. Features atomic file writes, file protection with read-only attributes, and pluggable RenderableModel classes for document rendering. Provides both command-line scripts and Python functions for applying patches to knowledge documents.

### Task Lifecycle Tool
Iteration-based task management system for tracking task execution through numbered iterations with automatic metrics collection. Collects code metrics from git diff (files changed, lines added/removed) and test metrics from pytest (pass rate, coverage). Tasks progress through iterations until metrics stabilize, then archive to history.

## Multiple Handlers

The plugin uses a modular handler structure with separate handler files in the `hooks/` directory:
- Each hook type has its own dedicated handler module
- Handlers are dynamically loaded and executed based on configuration
- New handlers can be added without modifying the core plugin logic
