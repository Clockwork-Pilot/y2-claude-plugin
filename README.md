# Claude Code Plugin

A minimal Claude plugin written in Python that implements hook handlers and logs all hook invocations.

## Features

- Logs all hook events to `hooks.log`
- Returns exit code 0 to allow Claude Code to proceed
- Separate handler configuration for each hook type
- Uses absolute paths for both interpreter and handlers

## Plugin Structure

```
.
├── .claude-plugin/
│   └── plugin.json          # Main plugin manifest
├── hooks/
│   ├── handler.py           # Unified hook handler (logs all events)
│   └── hooks.json           # Hook configuration reference
├── config.py                # Centralized path configuration
└── hooks.log                # Hook invocation logs (created at runtime)
```

## Implementation Details

### Hook Handler (hooks/handler.py)
- Reads hook input from stdin as JSON
- Logs event type, tool name, and argument keys
- Always returns exit code 0
- Handles JSON parse errors gracefully

### Plugin Manifest (.claude-plugin/plugin.json)
- Registers handlers for PreToolUse hooks: Write, Edit, Bash, Read, Glob, Grep
- Uses explicit absolute paths:
  - Python interpreter: `/home/yaroslav/local/python3/bin/python3`
  - Handler script: `/home/yaroslav/git/y2-claude-plugin/hooks/handler.py`

### Configuration (config.py)
- Single source of truth for project paths
- Configurable logging level (INFO, DEBUG, WARNING, ERROR, CRITICAL)

## Usage

The plugin automatically handles all registered hook events and logs them. View the logs:

```bash
tail -f hooks.log
```

## Supported Hooks

- `PreToolUse.Write` - Before file write operations
- `PreToolUse.Edit` - Before file edit operations
- `PreToolUse.Bash` - Before bash command execution
- `PreToolUse.Read` - Before file read operations
- `PreToolUse.Glob` - Before file glob pattern matching
- `PreToolUse.Grep` - Before file content searching
