# TASK-012: Agentic Meta-Skill Synthesis

## Description

Evolve the `init_skill.py` script into a more intelligent synthesis engine. Instead of just generating placeholders, this tool should use an LLM meta-prompt to draft the core logic, architectural patterns, and initial script boilerplate for a new meta-skill based on a high-level goal statement.

## Requirements

- **Synthesis Engine**: Create `scripts/synthesize_skill.py`.
- **Meta-Prompting**: Develop a robust system prompt that understands the "Skill Creator" standards (Conciseness, Degrees of Freedom, Progressive Disclosure).
- **Boilerplate Generation**: Automatically generate initial versions of `SKILL.md` and basic implementation scripts in `scripts/`.
- **Iterative Refinement**: Allow the user to provide feedback on the draft to refine it immediately.

## Acceptance Criteria

- [ ] `scripts/synthesize_skill.py` can generate a fully valid skill folder from a one-sentence input (e.g., "Create a meta-skill for AWS Lambda safety").
- [ ] Generated `SKILL.md` uses correct frontmatter and contains Zero TODOs (all context filled with high-quality drafts).
- [ ] Generated scripts are syntactically correct Python.
- [ ] Integration with the existing `package_skill.py` workflow.

## Technical Notes

- Use the current `SKILL.md` as the "few-shot" or "system context" for the generator.
- Ensure the output strictly follows the " imperative/infinitive form" guideline.
- Consider using an "Agentic Loop" (Draft → Internal Validate → Fix → Final Output).

## Definition of Done

- All acceptance criteria met.
- Successfully synthesized a new meta-skill (e.g., `cloud-auth-safety`) as a test.
- Tooling integrated into the root `skill-creator` meta-skill.
