# TASK-011: Automated Meta-Skill Evaluation

## Description

The `skill-creator` needs a way to verify that a generated meta-skill actually meets high-quality procedural standards. This task involves building an automated evaluation engine that "Red Teams" a meta-skill by simulating scenarios that test its logic, safety rails, and observability patterns.

## Requirements

- **Evaluator Engine**: Create `scripts/evaluate_skill.py` that can load a skill and run a set of "Chaos Monkey" tests against its scripts and workflows.
- **Verification Logic**: Logic to verify that if an agent follows the meta-skill, it correctly identifies failure modes (e.g., trips a circuit breaker).
- **Feedback Loop**: Generate a report status that identifies exactly where a meta-skill's logic is weak or incomplete.

## Acceptance Criteria

- [ ] `scripts/evaluate_skill.py` exists and is executable.
- [ ] Evaluation engine can simulate at least 3 failure types (API timeout, Auth failure, Data corruption).
- [ ] Engine provides a "Mastery Score" for the target meta-skill.
- [ ] Integration with `quick_validate.py` for a complete "CI/CD for Skills" experience.

## Technical Notes

- Use a "shadow execution" pattern where the script runs the meta-skill's logic in a mock environment.
- Focus on verifying the "Progressive Disclosure" principle (is the right info loaded at the right time?).
- Use `pytest` or a similar harness for the underlying test runners.

## Definition of Done

- All acceptance criteria met.
- Validated against the `agentic-orchestration` meta-skill.
- Re-packaged the meta-skill creator.
