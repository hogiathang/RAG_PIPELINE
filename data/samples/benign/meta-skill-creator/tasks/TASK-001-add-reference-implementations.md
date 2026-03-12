# TASK-001: Add Reference Implementations (scripts/)

## Description

The agentic-orchestration meta-skill currently provides conceptual guidance on safety controls (circuit breakers, rate limiters, etc.) but lacks concrete, executable implementations. Engineers implementing the framework need working reference code to understand the patterns and accelerate their development.

## Requirements

- **Circuit Breaker Implementation**: Python module implementing the circuit breaker pattern with configurable thresholds (failure count, timeout window, half-open state)
- **Rate Limiter Implementation**: Token bucket or sliding window rate limiter that can wrap agent operations
- **Idempotency Checker**: Utility to validate and enforce idempotent operations with request deduplication
- **Sandbox Manager**: Script to create and destroy ephemeral test environments for safe agent experimentation

Each implementation should be:
- Framework-agnostic (usable across different AI agent platforms)
- Well-documented with docstrings
- Include usage examples in comments

## Acceptance Criteria

- [ ] `scripts/circuit_breaker.py` exists with working implementation and unit tests
- [ ] `scripts/rate_limiter.py` exists with at least one algorithm implementation (token bucket or sliding window)
- [ ] `scripts/idempotency_checker.py` can track and prevent duplicate operations
- [ ] `scripts/sandbox_manager.py` can provision and tear down isolated environments
- [ ] Each script is executable standalone and includes example usage
- [ ] SKILL.md is updated to reference these new scripts

## Technical Notes

- Use Python 3.8+ for compatibility
- Avoid external dependencies where possible (use standard library)
- Consider thread-safety for concurrent agent operations
- Include type hints for better IDE support

## Definition of Done

- All acceptance criteria met
- All scripts tested by running them standalone
- Updated and re-packaged the meta-skill file
  ```bash
  python3 scripts/package_meta-skill.py agentic-orchestration
  ```
- Documentation in SKILL.md references new scripts
