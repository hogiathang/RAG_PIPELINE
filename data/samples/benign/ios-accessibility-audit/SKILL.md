---
name: ios-accessibility-audit
description: Audit iOS accessibility for screens and flows. Use to check Dynamic Type, VoiceOver, touch targets, contrast, focus order, and reduced motion (platform guidance, not implementation).
---

# iOS Accessibility Audit

## Overview
Audit a screen or flow for accessibility gaps and return prioritized fixes with RN/Expo implementation hints.

## Inputs to Request
- Scope: single screen or flow.
- Target devices (iPhone, iPad, or both).
- Any design system constraints.

## Audit Workflow
1. Run the checklist in `references/checklist.md`.
2. Map each issue to the relevant RN/Expo prop or pattern.
3. Prioritize fixes by severity: High, Medium, Low.

## Output Format
- Issues grouped by severity.
- Each item includes issue, fix, and RN/Expo hint.

## References
- `references/checklist.md`
- `references/rn-props.md`
