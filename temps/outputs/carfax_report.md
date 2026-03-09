# Agent Skill Security Analysis Report

## Overview
- Skill Name: keychains
- Declared Purpose: Call any API without leaking credentials. Keychains proxies requests and injects real tokens server-side — your agent never sees them.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The "keychains" skill describes and facilitates the use of a credential proxy service (`keychains.dev`) and its associated CLI/SDKs. Its stated purpose is to enhance security for AI agents by preventing them from directly handling sensitive API credentials. Instead, agents use placeholders, and the `keychains.dev` service injects real credentials server-side. While the skill itself is a benign set of instructions, its core functionality relies on trusting a third-party service and external software (npm packages), which introduces supply chain and data privacy risks.

## Observed Behaviors

### Behavior: External Tool Installation
- Category: Agent Manipulation (indirectly, by instructing agent to install external software)
- Technique ID (if applicable): SC2 — RemoteScriptExecution (potential risk from external package)
- Severity: LOW (for the skill's direct action) / MEDIUM (for the implied dependency risk)
- Description: The skill's `metadata.json` includes an `install_command` that downloads the `SKILL.md` file. However, the `metadata.openclaw.install` section and the `SKILL.md` content instruct the user/agent to install the `keychains` CLI tool globally via `npm install keychains@latest -g`.
- Evidence:
    - `metadata.json`: `"install_command": "mkdir -p .claude/skills/keychains && curl -sL \"https://raw.githubusercontent.com/openclaw/skills/main/skills/interagentic/keychains/SKILL.md\" > .claude/skills/keychains/SKILL.md"`
    - `SKILL.md`: `metadata: {"openclaw": {"emoji": "🔐", "homepage": "https://keychains.dev", "requires": {"bins": ["keychains"]}, "install": [{"id": "npm", "kind": "node", "package": "keychains@latest", "global": true, "bins": ["keychains"], "label": "Install Keychains CLI (npm)"}]}}`
    - `SKILL.md`: "Install Keychains CLI (npm)"
- Why it may be benign or suspicious: The `install_command` for the skill itself is benign (just downloads the markdown). The instruction to install `keychains` via `npm` is standard for CLI tools. However, as highlighted by the web search context ("Dangers of Trojanized NPM Packages in Development"), installing npm packages carries a supply chain risk. If the `keychains` npm package were compromised, it could lead to remote code execution on the system where it's installed. This is a general risk of using third-party software, not an inherent malicious action by *this skill's code*.

### Behavior: Credential Proxying
- Category: Data Handling / Credential Management
- Technique ID (if applicable): P3 — ContextLeakageAndDataExfiltration (potential if trust is broken)
- Severity: MEDIUM
- Description: The skill's core functionality involves proxying API requests through the `keychains.dev` service. The agent sends requests with placeholder credentials, which are then replaced by real credentials stored server-side at `keychains.dev` before being forwarded to the target API. This is designed to prevent the agent from ever seeing the real credentials.
- Evidence:
    - `SKILL.md`: "Keychains proxies requests and injects real tokens server-side — your agent never sees them."
    - `SKILL.md`: "Your request goes through keychains.dev, which replaces `{{PLACEHOLDER}}` variables with real credentials from the user's vault, forwards to the upstream API, and returns the response as-is. Real credentials never reach the agent."
    - Examples show usage with `{{OAUTH2_ACCESS_TOKEN}}`, `{{STRIPE_SECRET_KEY}}`, `{{OPENAI_API_KEY}}`.
- Why it may be benign or suspicious: This is the declared, legitimate purpose of the skill, aiming to *improve* security by abstracting credentials from the agent. However, it means that the `keychains.dev` service itself acts as a trusted third party that handles all real credentials and all API request/response data. Users must place full trust in the security and integrity of the `keychains.dev` service and its operators. If `keychains.dev` were compromised or malicious, it would facilitate credential theft and data exfiltration.

### Behavior: Network Communication
- Category: Network Interaction
- Technique ID (if applicable): E1 — ExternalTransmission (intended)
- Severity: LOW
- Description: The skill instructs the agent to make network requests using the `keychains` CLI/SDK, which then communicates with the `keychains.dev` service and subsequently with various third-party APIs (e.g., GitHub, Slack, Stripe, Gmail).
- Evidence:
    - `SKILL.md`: "keychains curl https://api.github.com/user/repos"
    - `SKILL.md`: "Authorize at: https://keychains.dev/approve/abc123xyz"
    - `SKILL.md`: "Your request goes through keychains.dev..."
- Why it may be benign or suspicious: This is fundamental to the skill's operation as an API proxy. The communication with `keychains.dev` is expected. The communication with various external APIs (GitHub, Slack, etc.) is also expected, as these are the target services the agent intends to interact with.

## Suspicious Indicators
- Sensitive data access: The `keychains.dev` service is designed to access and manage real API keys/tokens and process API request/response bodies. This is its explicit function, but it makes `keychains.dev` a high-value target for attackers and requires significant trust from the user.
- Network endpoints: `keychains.dev` is the central external endpoint. While legitimate for its purpose, it represents a single point of trust and potential failure.
- Dangerous commands/APIs: The instruction to use `npm install keychains@latest -g` carries the general supply chain risk associated with installing any third-party npm package, as highlighted by the web search context.

## Hidden or Undocumented Functionality
None detected. The skill's description is quite thorough in explaining its purpose, how it works (including the proxying mechanism and the role of `keychains.dev`), and how to use its various components (CLI, SDKs).

## Final Assessment
The "keychains" skill is classified as **BENIGN**. Its declared purpose is to provide a security-enhancing layer for AI agents by abstracting sensitive API credentials through a proxy service. The skill's code itself (the `SKILL.md` and `metadata.json`) primarily describes this functionality and provides instructions for installing and using the external `keychains` tool. It does not contain any directly malicious code or instructions for harmful actions.

However, the skill introduces a **MEDIUM** overall risk due to its reliance on a third-party service (`keychains.dev`) and external software (npm packages). Users must implicitly trust `keychains.dev` with their API credentials and all data exchanged with target APIs. The general risk of a compromised npm package (supply chain attack) also applies to the `keychains` CLI installation. These are inherent risks of using a credential proxy service, not indicators of malicious intent within the skill's provided definition.

## Recommended Action
**REVIEW**

The skill's concept is beneficial for agent security. However, due to the critical trust placed in the `keychains.dev` service and the supply chain risks associated with installing external npm packages, users should perform due diligence. This includes reviewing the security whitepaper, privacy policy, and terms of service of `keychains.dev`, and ensuring the integrity of the `keychains` npm package before installation. For high-security environments, the option to self-host a "Satellite proxy" (mentioned in the Product Hunt context) might be a preferred approach to mitigate some data privacy concerns.