---
name: ios-navigation-architecture
description: Choose and review iOS navigation patterns (tabs, stacks, modals, sheets, deep links). Use when designing app structure or refactoring navigation (platform guidance, not implementation).
---

# iOS Navigation Architecture

## Overview
Select a navigation structure that matches user goals, frequency, and depth.

## Inputs to Request
- Primary sections and their frequency of use.
- Expected depth within each section.
- Any need for modals or temporary tasks.
- Deep link requirements.

## Workflow
1. Apply the decision tree in `references/decision-tree.md`.
2. Validate against anti-patterns in `references/anti-patterns.md`.
3. Output the recommended structure and why it fits.

## Output Format
- Recommended navigation pattern.
- Rationale (1-2 sentences).
- Risks or trade-offs.

## References
- `references/decision-tree.md`
- `references/anti-patterns.md`
