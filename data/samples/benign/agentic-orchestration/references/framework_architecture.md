# Framework Architecture

The architectural framework that surrounds your application, enabling agents to operate it.

**Three layers**:

## Three-Layer Model

```
┌─────────────────────────────────────────────────────────────┐
│              AGENTIC FRAMEWORK (Orange)                     │
│   Safety & Control · Infrastructure · Observability         │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              SKILLS LAYER (Yellow)                  │   │
│   │   Domain Knowledge · Workflows · Tool Configs       │   │
│   │                                                     │   │
│   │   ┌─────────────────────────────────────────────┐   │   │
│   │   │         APPLICATION LAYER (Grey)            │   │   │
│   │   │   Database · APIs · Frontend · Backend      │   │   │
│   │   └─────────────────────────────────────────────┘   │   │
│   │                                                     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Layer | Purpose | Changes When |
|-------|---------|--------------|
| **Framework** | How agents operate safely | Infrastructure/safety requirements change |
| **Skills** | What agents know how to do | New domains, workflows, or tools needed |
| **Application** | What agents act upon | Business logic or features change |

## Framework Layer Components

### 1. Safety & Control
*   **Stop Hooks**: Mechanisms to immediately halt agent execution based on external triggers or internal anomaly detection.
*   **Circuit Breakers**: Automatic cut-offs that prevent cascading failures. If an agent fails `N` times in `T` seconds, the circuit opens and prevents further actions.
*   **Rate Limiting**: Throttling agent actions to prevent API quota exhaustion or system overload.

### 2. Infrastructure Harness
*   **Sandbox Environments**: Ephemeral, isolated environments where agents can plan and test changes before applying them to production.
*   **Idempotency Controls**: Ensuring that if an agent repeats an action (e.g., "create user"), the system state remains consistent and doesn't duplicate data.
*   **Infrastructure-as-Code (IaC) Integration**: Allowing agents to provision their own required resources via Terraform/Pulumi/etc. within safe bounds.

### 3. Observability & Analytics
*   **Distributed Tracing**: Tracking an agent's "thought process" and resulting actions across multiple services.
*   **Agent Versioning**: Managing different versions of agent prompts/models to rollback if a new version degrades performance.
*   **Audit Logging**: Immutable logs of every decision and tool call made by the system.

### 4. Meta-Skills
*   **Skill Creator**: Tools that generate and manage Skills (the yellow layer)
*   **Skill Registry**: Discovery and loading of available skills
*   **Skill Validation**: Ensuring skills meet quality and security standards

## Skills Layer Components

Skills are the "missing middle" - the domain intelligence that makes agents useful:

### Skill Anatomy
```
skill-name/
├── SKILL.md           # Frontmatter (name, description) + instructions
├── scripts/           # Executable code for deterministic tasks
├── references/        # Documentation loaded into context as needed
└── assets/            # Files used in output (templates, images)
```

### What Skills Provide
*   **Domain Knowledge**: Schemas, business logic, company-specific patterns
*   **Workflows**: Multi-step procedures (PDF editing, deployments, code review)
*   **Tool Configurations**: How to use specific APIs, libraries, or systems
*   **Bundled Resources**: Scripts, templates, and assets for complex tasks

### Skills vs Framework
| Concern | Framework | Skills |
|---------|-----------|--------|
| Scope | Universal (all agents) | Domain-specific |
| Updates | Infrastructure team | Domain experts |
| Example | Circuit breakers | `pdf-editor`, `bigquery` |

## The "Orange Box" Philosophy

The goal of the Agentic Framework is to treat the Agent not as a *user* of the software, but as an *operator* of the infrastructure.

*   **Users** click buttons in the Frontend.
*   **Agents** manipulate the database, deploy code, and reconfigure the load balancer.

Because Agents have this elevated privilege, the **Framework (Orange Box)** must provide the rigorous safety controls usually reserved for senior DevOps engineers, while **Skills (Yellow Layer)** provide the domain knowledge needed to operate effectively.
