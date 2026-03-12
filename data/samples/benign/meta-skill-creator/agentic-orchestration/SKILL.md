---
name: agentic-orchestration
description: Defines the three-layer architecture for the "Agentic Framework" - a meta-layer that surrounds an Application Layer with a Skills Layer in between, providing production-grade controls for AI agents. Use this skill when designing, explaining, or implementing agentic systems that require robust orchestration, domain capabilities, and safety controls.
---

# Meta-Skill: Agentic Orchestration

## Overview

The architectural framework that surrounds your application, enabling agents to operate it.

**Three layers**:
- **Framework** (orange): Production-grade controls - stop hooks, circuit breakers, observability
- **Skills** (yellow): Your workflows, conventions, and tool configurations
- **Application** (grey): Your codebase - the system agents operate on

## The Core Concept

The architecture consists of three distinct layers:

```
┌───────────────────────────────────────────────────────┐
│           AGENTIC FRAMEWORK (Orange)                  │
│    Orchestration · Safety · Observability · Lifecycle │
│                                                       │
│   ┌───────────────────────────────────────────────┐   │
│   │           SKILLS LAYER (Yellow)               │   │
│   │   Domain knowledge · Workflows · Capabilities │   │
│   │                                               │   │
│   │   ┌───────────────────────────────────────┐   │   │
│   │   │       APPLICATION LAYER (Grey)        │   │   │
│   │   │   Database · APIs · Frontend · Backend│   │   │
│   │   └───────────────────────────────────────┘   │   │
│   │                                               │   │
│   └───────────────────────────────────────────────┘   │
│                                                       │
└───────────────────────────────────────────────────────┘
```

### Layer 1: Application Layer (Grey - Innermost)
The target system that agents build, maintain, or operate:
- Database & data stores
- Frontend & Backend
- APIs & Microservices
- Mobile Apps
- Testing Infrastructure
- Documentation
- Scripts & DevOps configurations

### Layer 2: Skills Layer (Yellow - Middle)
The domain intelligence layer - the "missing middle" that makes agents actually useful:
- **Domain Knowledge**: Schemas, business logic, company-specific patterns
- **Workflows**: Multi-step procedures for specific tasks (PDF editing, deployments, code review)
- **Tool Configurations**: How to use specific APIs, libraries, or systems
- **Bundled Resources**: Scripts, templates, and assets for complex tasks

Skills are the interface between framework orchestration and application manipulation. They translate high-level agent intentions into domain-specific operations.

**Examples**: `pdf-editor`, `bigquery`, `deploy-aws`, `brand-guidelines`, `api-helper`

### Layer 3: Agentic Framework (Orange - Outermost)
The control plane that enables safe agentic operation:

**Key Capabilities:**
- **Production-Grade Controls**: Stop hooks, circuit breakers, rate limiting
- **Infrastructure Harness**: Idempotency controls, distributed tracing, sandbox environments
- **Lifecycle Management**: Agent versioning, monitoring, and analytics
- **Meta-Skills**: Tools that create and manage the Skills Layer (e.g., `skill-creator`)

## Why Three Layers?

The three-layer model solves a fundamental problem: **agents need domain knowledge to be useful, but that knowledge shouldn't be baked into the control plane**.

| Layer | Concern | Changes When... |
|-------|---------|-----------------|
| Framework | How agents operate safely | Infrastructure/safety requirements change |
| Skills | What agents know how to do | New domains, workflows, or tools are needed |
| Application | What agents act upon | Business logic or features change |

This separation enables:
- **Independent evolution**: Update skills without touching framework infrastructure
- **Reusable skills**: Same `pdf-editor` skill works across different applications
- **Clear boundaries**: Framework team focuses on safety, domain experts create skills

## Framework Architecture

For detailed architectural patterns and component definitions, see:
[references/framework_architecture.md](references/framework_architecture.md)

## Implementation Guide

When implementing this architecture, follow these core principles:

### Layer Isolation
1. **Framework ↔ Skills**: The framework orchestrates skill execution but doesn't contain domain logic. Skills are loaded dynamically based on context.
2. **Skills ↔ Application**: Skills define *how* to interact with the application, but don't contain application state or business logic.
3. **Failure boundaries**: Each layer can fail independently without cascading. A skill error doesn't crash the framework; a framework restart doesn't corrupt application data.

### Core Principles
1. **Observability**: Every action taken by an agent must be traced, logged, and reversible where possible.
2. **Safety First**: Implement "circuit breakers" that cut off agent access if error rates spike or destructive commands are attempted.
3. **Progressive Enhancement**: Start with minimal skills (Grade 1.2), add custom tools (Grade 1.3), then feedback loops (Grade 1.4).

## Usage

Use this skill to:
- **Architect new agentic systems**: Reference the three-layer model for clear separation of concerns
- **Design the Skills Layer**: Identify what domain knowledge should be captured as reusable skills
- **Audit existing systems**: Check if skills are properly isolated from both framework and application
- **Explain the pattern**: Use the "Orange / Yellow / Grey" visual to explain agentic orchestration to stakeholders
- **Plan migrations**: Determine which grade level is appropriate based on skill complexity needed
