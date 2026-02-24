# Claude Code Plugin

A minimal Claude plugin written in Python that implements hook handlers and logs all hook invocations.

## Features

- Logs all hook events to `hooks.log`
- Returns exit code 0 to allow Claude Code to proceed
- Separate handler configuration for each hook type
- Uses absolute paths for both interpreter and handlers
