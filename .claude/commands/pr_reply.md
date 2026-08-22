---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(tree), Bash(git:*), Bash(cat:*), Bash(find:*), Bash(gh pr view), Bash(gh pr:*), Bash(gh api), Bash(gh pr review)
description: Respond to PR review comments with fixes and detailed explanations
---

## Context
- Current directory: !`pwd`
- Repository status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Changed files in PR: !`git diff --name-only HEAD~1`
- Recent commits: !`git log --oneline -5`

## Task

You are a senior engineer responding to PR review feedback. Your goal is to address all review comments professionally and thoroughly. Not every comment requires a code change. Only make a code change if the commenter asks for it. If there is a question, this is a good indicator that a code change is not needed.

### Process

1. **Fetch PR Details**: Retrieve and analyze review comments for PR number: #$ARGUMENTS
2. **Categorize Comments**: Identify whether each comment requires:
   - Code fixes/changes
   - Clarifying questions/answers
   - Technical explanations
   - Documentation updates

3. **Address Each Comment**:
   - **For suggested fixes**: Implement the change, test if applicable, and reply confirming the fix
   - **For questions**: Provide comprehensive answers with code examples or references when helpful
   - **For explanation requests**: Give detailed technical explanations with context and reasoning
   - **For discussions**: Engage constructively, providing alternative solutions when appropriate

### Guidelines

- **Code Changes**: 
  - Make precise, targeted fixes
  - Ensure changes align with existing code style
  - Test changes when possible
  - Commit with descriptive messages referencing the review

- **Responses**:
  - Be respectful and professional
  - Provide context and reasoning for decisions
  - Include code snippets or file references when relevant
  - Ask for clarification if comments are ambiguous

### Output Format

For each review comment:
1. Respond directly to the comment at the individual line.
2. Provide your response/action taken
3. Include relevant code changes or explanations
4. Mark as resolved when appropriate
5. If changes are made, make sure to commit and push changes to the PR branch.