# TASK-015: Self-Healing Auditor Mesh

## Description

Move from "Top-Down" orchestration to a "Peer-to-Peer" governance model. This task involves setting up a dual-agent configuration where one agent (the Operator) performs the work, and a second "ghost" agent (the Auditor) lives inside the framework boundary. The Auditor uses meta-skills as its "Legal Code" to monitor the Operator in real-time.

## Requirements

- **Auditor Definition**: Create a specific Auditor Agent configuration that prioritizes safety and compliance over task completion.
- **Inter-Agent Communication Protocol**: A low-latency channel where the Auditor can "veto" or "request clarification" from the Operator before commands are finalized.
- **Self-Healing Logic**: If the Auditor trips a circuit breaker, it can automatically trigger a "Rollback Script" defined in the meta-skill to restore the application state.
- **Conflict Resolution**: Logic for when the two agents disagree on the safety of an action.

## Acceptance Criteria

- [ ] Successful "Audit Veto": The Auditor agent blocks an action from the Operator agent and suggests a safer alternative.
- [ ] The Auditor agent provides "Compliance Justification" citing specific lines from the meta-skills.
- [ ] Demonstration of "Self-Healing": Auditor triggers a rollback after a simulated operator error.

## Technical Notes

- The Auditor should ideally use a "cheap" but high-reasoning model to minimize costs.
- Ensure the Auditor has "Read-Only" access to the app but "Write" access to the Framework's safety hooks.
- Focus on the "Orange Box" philosophy: the Auditor is part of the framework, not the user session.

## Definition of Done

- All acceptance criteria met.
- Multi-agent simulation successfully runs a "Safe Deployment" scenario.
- Meta-skills updated with "Auditor Scrutiny" patterns.
