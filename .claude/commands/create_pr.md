---
allowed-tools: Bash(git:*), Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git branch:*), Bash(git log:*), Bash(gh pr:*), Bash(git diff:*)
description: Create a git PR for the current branch
---

## Context

- Current git status: !`git status`
- Current default branch: !`git remote show origin | grep "HEAD branch"`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`


## Task

Review the current git status and diff against the default branch, and use the gh pr create command to create a PR for the current branch. Use the spec and your memory to fill in the blanks. After creating the PR, if there is a CHANGELOG.md file, update it with the changes in this PR. Make sure the dates match the commit or PR dates.

## Template:

## PR Type

- fix, feature

## Summary

- Provide a file by file summary of the changes in the following table. Be sure to use the git diff command to determine what changed.

Format:
  | File Name | Change Summary |
  | --- | --- |
  | src/file1.ts | Added a new function to the file |
  | src/file2.ts | Updated the file to use the new function |
  | src/file3.ts | Refactored for style/formatting; no logic changes. |
  | ... | ... |

- Be sure to only describe the changes that occured in each file during this PR. Do not summarize what the file does. Use the available tools to determine what changed.

## Linear Tickets (optional)

- [Ticket here](link.com)

## Breaking Changes

- No breaking changes

## Edge Cases for Reviewer

- Provide a list of potential edge cases that the reviewer should consider. These should be edge case the occur because of the changes in this PR. Include the code samples and the expected behavior. Each edge case should follow the format:

    - File path
    - Line numbers
    - Brief description of the edge case including why this may be an issue. It is important to include the potential impact of the edge case on the system or user experience.
    - Block of affected code using code block syntax
    - Prompt for AI agent to fix the edge case. This should include the file path, line numbers, and a detailed description of the fix.

Here is an example response:

    File path: frontend/src/routes/organizations/[id]/+page.svelte
    Line numbers: 36 to 52
    Description: Replace mock organization data with API call. The organization object is currently mocked. Consider implementing a dedicated endpoint for fetching single organization details.
    
    Affected code:
    ```typescript
        organization = {
            id: id,
            name: "DAO Organization", // This would come from API
            slug: `dao-org-${id}`,
            proposals_count: proposals.length,
            chain_ids: ["ethereum", "polygon"],
            token_ids: [],
            governor_ids: [],
            metadata: null,
            endorsement_service: null,
            has_active_proposals: false,
            delegates_count: 0,
            delegates_votes_count: "0",
            token_owners_count: 0
        };
    ```
    Prompt for AI Agent:
    ```
    In frontend/src/routes/organizations/[id]/+page.svelte around lines 36 to 52,
    replace the hardcoded mock organization object with an actual API call to fetch
    the organization details by its id. Implement or use an existing endpoint that
    returns the single organization's data, then assign the fetched data to the
    organization variable instead of the mock object.
    ```
    - If no edge cases are found, say "No edge cases found"

## Reviewer Test Plan
- Provide a list of tests or processes the human reviewer should consider to be confident in the changes.

- [ ] Test Case 1
- [ ] Test Case 2
- [ ] Test Case 3

- Add labels to the PR. Here are the labels [bug, documentation, enhancement]: `gh pr create -l "bug"`

## Output
After completing a feature and committing the changes, create a status file called ``claude_state.json`` in 
`.claude/river/`. This will provide a way to track the progress of the project. It should be in the format below:

Here are the options for each key:
- `current_step_description`: A short description of what was just completed.
- `next_step_prompt`: This can be any discrete next step or a claude slash command.
- `status`: The status of the current step, either "running" or "completed". If a PR is successfully created, set this to "completed".

```json
{
    "orchestrator_id": null,
    "current_step_description": "Created a PR for the current branch",
    "next_step_prompt": "Description of the work that needs to be done, if any.",
    "status": "completed"
}
```