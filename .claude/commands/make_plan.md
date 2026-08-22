---
allowed-tools: Bash(grep:*), Bash(ls:*), Bash(tree), Bash(git:*), Bash(find:*)
description: Make a plan from linear.
---

## Context
- Linear Parent Issue ID: $LINEAR_ID

## Task
You are a details and thorough Technical Product Manager with an eye for elegant simple solutions. Create a detailed implementation plan for the Linear parent and sub issues. The plan should break down the work into granular, TDD-friendly tasks. Using the linear MCP server that you have access to, access details about these issues then follow the steps below. Take care to not over engineer the plan. The most elegant  solutions are the simplest ones that solve the problem with the least amount of code or changes needed.

## Simplicity
Before creating plan.md, double-check your work. We want a minimal, no-frills implementation of the linear issues. Review plan.md 
and make sure that we are keeping our changes to a minimum and that this implementation is as simple as possible to meet the goals 
of the linear story. Remove anything that you deem unnecessary. Think hard about this. DO NOT OVERENGINEER THE SOLUTION. Only include critical path items in the plan. This does not have to be a perfect production deployment focus on getting the functionality implemented.

## Steps

Steps:
- Mark the Linear issue as "In Progress"

1. **Deep Technical Analysis** (Use sub-agent)
   - Study all relevant specifications in `specs/` directory
   - Document key technical requirements and constraints
   - Identify dependencies and integration points

2. **Codebase Study** (Use sub-agent)
   - Analyze existing code structure and patterns
   - Map out affected modules and their relationships
   - Identify reusable components and potential refactoring needs

3. **Create Detailed plan.md**
   Generate a plan.md file in the root directory with the following structure:
   - Overview section with issue summary and objectives
   - Prioritized feature list (P0-P3 priority levels)
   - Each feature broken into atomic tasks
   - Each task formatted for one TDD cycle:
     * Clear acceptance criteria
     * Test cases to write
     * Implementation steps
     * Integration points
   - Risk assessment and mitigation strategies
   - Success criteria checklist
   - Resource estimates

Task Granularity Requirements:
- Each task should be completable in one TDD cycle (red-green-refactor)
- Include specific test names, expected behaviors, and justification for testing
- Define clear input/output boundaries
- Specify any API changes or new interfaces
- Do not over engineer the solution. The best solutions address the problem with the least amount of code possible.
- After you have created plan.md, double-check your work. We want a minimal, no-frills implementation of the linear issues. Review plan.md and make sure that we are keeping our changes to a minimum and that this implementation is as simple as possible to meet the goals of the linear story. Remove anything that you deem unnecessary. Think hard about this. 

## Output
- After completing a feature and committing the changes, create a status file called ``claude_state.json`` in 
`.claude/river/`. 
- It should follow the following format with these values:

```json
{
    "current_step_description": "Made a plan.md file",
    "next_step_prompt": "/ralph",
    "status": "running"
}
```