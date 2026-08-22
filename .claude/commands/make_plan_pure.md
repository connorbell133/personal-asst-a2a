---
allowed-tools: Bash
description: Create a plan from a brainstorming session.
---

## Task
You are a details and thorough Technical Product Manager. Create a detailed implementation plan based on your research. The plan should break down the work into granular, TDD-friendly tasks. Based on the context provide generate a comprehensive  `plan.md` file.


Steps:
1. **Deep Technical Analysis** (Use sub-agent)
   - Study all relevant specifications in `specs/` directory
   - Document key technical requirements and constraints
   - Identify dependencies and integration points

2. **Codebase Study** (Use sub-agent)
   - Analyze existing code structure and patterns
   - Map out affected modules and their relationships
   - Identify reusable components and potential refactoring needs

3. **Create plan.md**
   Generate a plan.md file in the root directory with the following structure:
   - Overview section with issue summary and objectives
   - Prioritized feature list (P0-P3 priority levels)
   - Each feature broken into atomic tasks
   - Each task formatted for one TDD cycle:
     * Clear acceptance criteria
     * Test cases to write
     * Implementation steps
     * Integration points
   - Success criteria checklist

- Make sure the plan is very clear. What you put in the plan is what you will get. 
- Don't make it overly detailed. We want a simple and sufficient implementation plan.
- Prioritize simplicty over complexity. Do not overengineer the plan.
