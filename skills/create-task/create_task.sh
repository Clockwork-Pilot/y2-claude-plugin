#!/bin/bash
# Noop script that prints the task name in JSON format
TASK_NAME="$1"

if [ -z "$TASK_NAME" ]; then
  echo '{"error": "Task name is required"}'
  exit 1
fi

echo "{\"task\": \"$TASK_NAME\"}"
