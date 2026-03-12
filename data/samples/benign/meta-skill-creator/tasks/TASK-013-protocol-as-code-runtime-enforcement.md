# TASK-013: Protocol-as-Code (Runtime Enforcement)

## Description

Transform static meta-skill documentation into an executable "Hard Contract." Currently, `SKILL.md` is advisory. This task involves building a runtime parser and validation proxy that enforces the rules defined in a meta-skill (like tool-use constraints or safety patterns) by intercepting and potentially blocking agent actions that violate the protocol.

## Requirements

- **Protocol Parser**: Build a parser that extracts "enforcement rules" from `SKILL.md` (e.g., specific tool-call limits, mandatory health checks, or forbidden flags).
- **Validation Proxy**: Implement a middleware layer that intercepts `run_command` or other tool calls.
- **Enforcement Engine**: Logic to compare the intercepted tool call against the extracted rules and return an "Enforcement Error" to the agent if violated.
- **Rule Annotation**: Define a standard markdown syntax for "enforceable" sections in `SKILL.md`.

## Acceptance Criteria

- [ ] `scripts/enforce_protocol.py` exists as a middleware utility.
- [ ] A tool call that violates a meta-skill's "Degrees of Freedom" is intercepted and blocked.
- [ ] The agent receives a structured error explaining which meta-skill rule was violated.
- [ ] Documentation updated to explain how to mark sections of a skill as "Enforceable."

## Technical Notes

- Use a JSON-Schema mapping for the extracted rules.
- Ensure the proxy adds minimal latency to the agentic loop.
- Consider "dry-run" vs "enforcement" modes.

## Definition of Done

- All acceptance criteria met.
- Validated by blocking a forbidden "recursive delete" command defined in an `agentic-orchestration` safety rule.
- Repackaged the meta-skill creator.
