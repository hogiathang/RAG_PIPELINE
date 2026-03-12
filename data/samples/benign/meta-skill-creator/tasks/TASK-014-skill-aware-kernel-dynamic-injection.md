# TASK-014: Skill-Aware Kernel (Dynamic Injection)

## Description

Eliminate context bloat by building an intelligent kernel that manages "Skill Hot-Swapping." Instead of loading all meta-skills at startup, the system acts as a "Skill-Aware OS" that detects the agent's current intent/file-access and dynamically injects the relevant meta-skill into the conversation context just-in-time.

## Requirements

- **Intent Monitor**: A layer that scans the agent's input and proposed actions for "intent triggers" (e.g., keywords like "database", "deploy", "audit").
- **Dynamic Context Manager**: A utility that can patch the current system prompt or context window to add/remove `SKILL.md` content on the fly.
- **Resource Sharding**: Standards for splitting large meta-skills into shards that can be loaded independently based on narrow sub-tasks.
- **Cache & Eviction**: Logic to "evict" skills that have not been used recently to keep the token count low.

## Acceptance Criteria

- [ ] `scripts/skill_kernel.py` prototype that manages context injection.
- [ ] Successful demonstration of a "Skill Swap": Agent moves from Python coding to AWS deployment, and the kernel replaces the `coding-standard` skill with `cloud-safety`.
- [ ] Dramatic reduction in baseline token usage for multi-skill systems.

## Technical Notes

- High performance is key; intent detection should be lightweight (likely regex or embedding-based classification).
- Keep a "Meta-Manifest" of available skills for the Kernel to look up.
- Handle "Skill Conflicts" where two skills might provide overlapping or contradictory instructions.

## Definition of Done

- All acceptance criteria met.
- Successfully managed a context-constrained session with 10+ available meta-skills.
- Packaging updated to include the Kernel as a "Meta-Orchestration" tool.
