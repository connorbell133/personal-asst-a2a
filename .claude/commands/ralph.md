---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(tree), Bash(git:*), Bash(find:*)
description: Implement and issue from plan.md
---

## Context
- Current directory: !`pwd`
- plan.md location: !`find . -name "plan.md"`

## Primary Task
You are a very senior software engineer. You are an expert in implementing simple but powerful software systems. Select and implement the highest priority unimplemented feature from `plan.md` using Test-Driven Development (TDD) methodology. Select and implement one thing and one thing only. Remember you can always right the status to `claude_status.json` to continue working on the next feature later.

SELECT AND IMPLEMENT ONE AND ONLY ONE TASK FROM `plan.md`.

Remember just because something is marked as implemented in `plan.md` does not mean it is implemented in the codebase. Always double check.

USE UP TO 5 SUBAGENTS FOR THIS TASK!

## Step-by-Step Process

### 1. Analysis Phase
- Use a subagent to read `plan.md` to understand all planned features
- Use a subagent to study relevant specifications in `specs/` directory
- Identify features that are not yet implemented
- Select the highest priority feature based on:
  - Dependencies (implement prerequisites first)
  - Business value indicators in the plan
  - Technical complexity considerations

### 2. Implementation Phase (TDD Approach)
- Only select features from `plan.md`. If its all implemented return the `/verify` command in `claude_state.json`
- RED: Write failing tests FIRST for the selected feature. For each test, write why the test is important and what it is testing in the docstring.
- GREEN: Implement minimal code to make tests pass
- REFACTOR: Refactor while keeping tests green

### 3. Completion Phase
- Update `plan.md` to mark the feature as "implemented"
- Include any relevant notes
- Commit all changes with descriptive commit message
- Add a comment to the Linear issue as to the current progress. This can be brief. If you don't know the linear issue then skip updating linear.

## Subagent Usage Guidelines
- You may use up to 3 subagents in parallel each responsible for an isolated RED - GREEN - REFACTOR cycle.

## Success Criteria
- [ ] Items from `plan.md` is fully implemented with passing tests
- [ ] `plan.md` is updated with implementation status
- [ ] All changes are committed to version control
- [ ] Code follows existing project conventions


## Commit Message Format
```
feat: Implement [feature name] from plan.md

- Added comprehensive test suite
- Implemented core functionality
- Updated plan.md status to 'implemented'
- Follows TDD methodology
```

## Test and Build
- If the language allows you to build the application such as Go, Rust, or TypeScript, build the application after each feature is implemented and debug accordingly. Do not complete the feature until the application builds successfully.

## Self Improvement
When you learn something new about how to run the application or examples make sure you update @CLAUDE.md using a subagent but keep it brief. For example if you run commands multiple times before learning the correct command then add the command to @CLAUDE.md

## Output
After completing a feature and committing the changes, create a status file called ``claude_state.json`` in 
`.claude/river/`. This will provide a way to track the progress of the project. It should be in the format below:

Here are the options for each key:
- `current_step_description`: string - A short description of what was just completed.
- `next_step_prompt`: string - Default to `/ralph` until plan.md is fully implemented. `/ralph` will run another plan.md implemntation cycle.
    - Once plan.md is fully implemented, this should be set to `/verify`. `/verify` will run the verification cycle to ensure plan.md is fully implemented.
    - If something else needs to be done then use the `/other <description of work to be done>` command. 
- `status`: string - The status of the current step, either "running" or "completed".

```json
{
    "current_step_description": "Implemented task 1 from plan.md",
    "next_step_prompt": "/ralph",
    "status": "running"
}
```

You cannot mark status as "completed" if you also mark next_step_prompt as "/verify" or "/ralph".
