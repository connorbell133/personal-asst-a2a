---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(tree), Bash(git:*), Bash(find:*)
description: Catchall command for river coding agent.
---

## Context
You are a helpful senior software engineer. You will be given a task to execute. Follow the steps below.

## Task
- $TASK

## Steps
1. Review the commit and git history for this branch.
2. Use a subagent to study the `specs/` directory to understand the specifications for the project.
3. Create a TODO list to execute the task.

## Output
After completing a feature and committing the changes, create a status file called ``claude_state.json`` in 
`.claude/river/`.  This will provide a way to track the progress of the project. It should be in the format below:

Here are the options for each key:
- `current_step_description`: string - A short description of what was just completed.
- `next_step_prompt`: string - If something else needs to be done then use the `/other <description of work to be done>` command. 
- `status`: string - The status of the current step, either "running" or "completed". Set to "completed" if all work is done.

```json
{
    "current_step_description": "Implemented task 1 from plan.md",
    "next_step_prompt": "/ralph",
    "status": "running"
}
```