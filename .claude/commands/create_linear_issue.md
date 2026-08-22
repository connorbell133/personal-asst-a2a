---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(tree), linear-server:*, Bash(linear-server:*)
description: Create a linear issue based on the research you've done.
---

## Context
- Current directory: !`pwd`
- Current files: !`ls -la`
- Current tree: !`tree`
- Linear Project: #$ARGUMENTS


## Task

First create a parent issue detailing the high level feature we are implementing.

Then generate linear sub-issues based on the research you've done. Make sure it is detailed and throughout. Think a lot about how to accomplish the task and describe it correctly so a junior developer can understand it and implement it. User the linear MCP to add the story to the team and project.`

Each issue should be a distinct task but if there are multiple tasks that are related to each other note that below. Make sure dependent issues are marked as blocked by the issue they depend on. If issues rely on each other, make sure the are added in sequence to linear.

Add all issues to the todo section in Linear.

As needed, create an issue and add sub-issues if it logically makes sense.

## Template:

User Story: Provide a user story for the issue.
Work to be done: Provide a detailed description of the work to be done.
Location of changes: Provide a detailed description of the location of the changes.
Definition of done: Provide a definition of done for the issue in a checklist format.
Functional Testing Strategy: A strategy for testing the functionality of the issue works. This should be a real world test.
Related issues: Provide a list of related issues.



