---
name: ios-screen-review
description: Structured iOS UX/UI review checklist. Use to critique hierarchy, spacing, affordances, copy, and states and output prioritized fixes (platform guidance, not implementation).
---

# iOS Screen Review

## Overview
Review a single screen or flow and return a prioritized list of UX/UI fixes.

## Inputs to Request
- Screen goal and primary action.
- Target device set (iPhone, iPad, or both).
- Known states: loading, empty, error, offline.
- Any constraints (brand rules, shared design system).

## Review Workflow
1. Run the checklist in `references/review-checklist.md`.
2. Flag issues by severity: High, Medium, Low.
3. Provide concrete fixes and a short rationale.
4. Include a quick win list if any changes are low effort and high impact.

## Output Format
- Issues and recommendations grouped by severity.
- Each item includes: issue, fix, and expected impact.

## References
- `references/review-checklist.md`
