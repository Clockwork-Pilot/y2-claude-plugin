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
    -v $HOME/.ssh/id_ed25519.pub:/home/node/.ssh/id_ed25519.pub:ro \
    -v $SSH_AUTH_SOCK:/ssh-agent \
    -e SSH_AUTH_SOCK=/ssh-agent \
    -v $(pwd)/.credentials:/home/node/:Z  \
    -v $(pwd):/project y2-coder

# Use forwarded SSH Key Inside of container
ssh-add -l
ssh-add ~/.ssh/id_ed25519

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
