---
name: create-task
description: Create a task by name and execute a script that prints it in JSON format. Use this whenever the user says "create a task", "make a task", "new task", or asks to create something with a name. Extract the task name from the user's prompt. The output will be JSON format: { "task": "task name" }
compatibility: bash
---

# Create Task Skill

This skill extracts a task name from the user's input and executes a script that outputs the task information in JSON format.

## How it works

1. **Extract the task name** from the user's prompt. Look for patterns like:
   - "Create a task 'task name'"
   - "Make a task: task name"
   - "New task called task name"
   - Any other natural phrasing that mentions a task name

2. **Execute the script** with the extracted task name as an argument

3. **Return the JSON output** in the format: `{"task": "task name"}`

## Example

**User input:** `Create a task 'Deploy to production'`

**Steps:**
1. Extract task name: `Deploy to production`
2. Execute: `./skills/create-task/create_task.sh "Deploy to production"`
3. Output: `{"task": "Deploy to production"}`

## Usage

The skill can be invoked in two ways:

### Implicit (from prompt)
User mentions a task name in their message, and the skill extracts it automatically.

### Explicit (from argument)
If the skill is called with an explicit argument, use that as the task name instead.

## Task Name Rules

- The task name should be extracted as-is from the user's input
- Remove quotes if they're used for clarity
- Handle various natural language patterns
