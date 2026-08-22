---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(git commit:*), WebFetch(domain:*), Write(file:*)
description: You are tasked with implementing a feature/fix for the following linear issue using a strict test-driven development (TDD) approach. Follow the Red-Green-Refactor cycle throughout the implementation.
---

## Context
- Current directory: !`pwd`
- Current files: !`ls -la`
- Linear Project: #$ARGUMENTS


## Instructions

You must first pull the linear issue using the linear-server MCP and mark it as "In Progress".

### 1. Analyze the Requirements
- Break down the issue into testable units
- Identify edge cases and error scenarios
- List all the behaviors that need to be implemented

### 2. Follow TDD Cycle for Each Behavior

#### a) Red Phase (Write Failing Test)
- Write a test that describes the expected behavior
- Run the test to ensure it fails with the expected error
- The test should be minimal and test only one behavior

#### b) Green Phase (Make Test Pass)
- Write the minimum code necessary to make the test pass
- Don't add extra functionality not required by the current test
- Run the test to ensure it passes

#### c) Refactor Phase
- Improve code quality while keeping tests green
- Remove duplication
- Improve naming and structure
- Run all tests to ensure nothing broke
- Decompose methods into smaller methods if needed
- No method should be more than 60 lines

#### d) Commit Phase
- Commit the changes to the repository
- The commit message should be a short description of the changes made
- The commit message should be in the format of "feat: add feature" or "fix: fix bug"
- The commit message should be in the language of the codebase
- The commit message should be in the present tense
- The commit message should be in the active voice

### 3. Implementation Order
- Start with the simplest test case
- Progress to more complex scenarios
- Handle edge cases last
- Write integration tests after unit tests

### 4. Test Structure Requirements
- Use descriptive test names that explain what is being tested
- Follow AAA pattern (Arrange, Act, Assert)
- Include both positive and negative test cases
- Test edge cases and error conditions

### 5. Code Requirements
- Follow existing code style and conventions
- Add appropriate documentation/comments
- Ensure all new code has test coverage
- Update any affected existing tests
- Always use the latest stable and compatible version of a package. Use a subagent to search the web for the latest version.

## Deliverables

1. Test file(s) with comprehensive test coverage
2. Implementation code that satisfies all tests
3. Brief explanation of your TDD process for each major component
4. List of any assumptions made during implementation

## Additional Guidelines

- **Commit Frequently**: Make a commit after each successful test implementation.
- **Test Isolation**: Ensure tests don't depend on each other
- **Mock External Dependencies**: Use mocks/stubs for external services
- **Verify UI Features**: Use the playwright MCP to verify the UI features by taking screenshots and comparing them to the expected state.

Please proceed with implementing the issue, showing each TDD cycle clearly.