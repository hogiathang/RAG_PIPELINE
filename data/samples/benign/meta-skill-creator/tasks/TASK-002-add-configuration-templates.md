# TASK-002: Add Configuration Templates (assets/)

## Description

The agentic-orchestration meta-skill provides architectural patterns but lacks ready-to-use configuration templates that engineers can copy and adapt for their specific implementations. Configuration templates would accelerate adoption by providing concrete starting points for common scenarios.

## Requirements

- **Circuit Breaker Configuration**: YAML template with sensible default thresholds (failure counts, timeout windows, recovery policies)
- **Agent Permissions Template**: JSON schema for RBAC-style permissions defining what operations agents can perform on different resources
- **Monitoring Dashboard Template**: Exportable dashboard configuration (Grafana/Datadog/Prometheus format) for agent observability metrics
- **Architectural Diagrams**: Visual representation of the Orange Box (Agentic Framework) / Grey Box (Application Layer) concept

Each template should:
- Include inline comments explaining all configuration options
- Provide sensible defaults based on common use cases
- Be framework-agnostic where possible

## Acceptance Criteria

- [ ] `assets/circuit_breaker_config.yaml` exists with documented configuration options
- [ ] `assets/agent_permissions.json` exists with example permission hierarchy
- [ ] `assets/monitoring_dashboard.json` exists for at least one monitoring platform
- [ ] `assets/architecture_diagram.png` visually shows the two-layer framework
- [ ] SKILL.md is updated to reference these new templates
- [ ] Templates are validated (YAML/JSON syntax check)

## Technical Notes

- Keep YAML/JSON configurations simple and readable
- For the architecture diagram, consider using the uploaded image as a starting point
- Include version comments in templates for future updates
- Ensure templates work across different tech stacks (Docker, Kubernetes, serverless)

## Definition of Done

- All acceptance criteria met
- All template files are syntactically valid
- Updated and re-packaged the meta-skill file
  ```bash
  python3 scripts/package_meta-skill.py agentic-orchestration
  ```
- Documentation in SKILL.md includes usage examples for templates
