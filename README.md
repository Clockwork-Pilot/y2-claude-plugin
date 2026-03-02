# Claude Code Plugin

A minimal Claude plugin written in Python that implements hook handlers and logs all hook invocations.

## Run in docker
Use docker image from this repo: github.com:YuraLitvinov/y2-docker-claude
Build & Run docker container as specified in their readme.

```
mkdir $(pwd)/.credentials -p && \
  docker run -it --rm  \
    --user 1000:1000  \
    -w /project \
    -v $SSH_AUTH_SOCK:/ssh-agent \
    -e SSH_AUTH_SOCK=/ssh-agent \
    -v $(pwd)/.credentials:/home/node/:Z  \
    -v $(pwd):/project y2-coder

# Inside of container - init specify for project
cd /project && \
  specify init --here --ai claude

# Inside of container - run claude
cd /project && \
  source .venv/bin/activate &&   claude --model claude-haiku-4-5 --debug --plugin-dir /project
```

## Features

- Logs all hook events to `hooks.log`
- Returns exit code 0 to allow Claude Code to proceed
- Separate handler configuration for each hook type
- Uses absolute paths for both interpreter and handlers

## Multiple Handlers

The plugin uses a modular handler structure with separate handler files in the `hooks/` directory:
- Each hook type has its own dedicated handler module
- Handlers are dynamically loaded and executed based on configuration
- New handlers can be added without modifying the core plugin logic
