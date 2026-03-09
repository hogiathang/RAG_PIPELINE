# Agent Skill Security Analysis Report

## Overview
- Skill Name: keychains
- Declared Purpose: Call any API without leaking credentials. Keychains proxies requests and injects real tokens server-side — your agent never sees them.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The "keychains" skill is designed to enhance the security of AI agents by acting as a credential proxy. It prevents the agent from directly handling sensitive API keys and OAuth tokens by replacing them with placeholders that are resolved and injected server-side by the `keychains.dev` service. While the skill's stated purpose is a security benefit, its reliance on an external service and the installation of an external binary/SDK introduce inherent supply chain and third-party trust risks. The skill's code itself does not exhibit malicious behavior.

## Observed Behaviors

### Behavior: Credential Proxying
- Category: Legitimate Functionality (Security Enhancement)
- Technique ID (if applicable): N/A
- Severity: LOW (Benign)
- Description: The core functionality of the skill is to proxy API requests, replacing credential placeholders (e.g., `{{OAUTH2_ACCESS_TOKEN}}`) with actual credentials server-side. This is explicitly designed to prevent the agent from directly accessing sensitive tokens.
- Evidence: "Keychains proxies requests and injects real tokens server-side — your agent never sees them." and "No credentials ever pass through the agent."
- Why it may be benign or suspicious: This behavior is explicitly declared as a security feature to protect credentials from the agent. It is benign if the `keychains.dev` service itself is trustworthy and securely managed.

### Behavior: External API Communication
- Category: Network Communication
- Technique ID (if applicable): E1 — ExternalTransmission (Legitimate)
- Severity: LOW (Benign)
- Description: The skill facilitates communication with various external APIs (e.g., GitHub, Slack, Stripe, Gmail) by routing requests through the `keychains.dev` proxy. It also communicates with `keychains.dev` for credential resolution and user approval.
- Evidence: Examples like `keychains curl https://api.github.com/user/repos`, `https://slack.com/api/chat.postMessage`, `https://api.stripe.com/v1/customers`, `https://gmail.googleapis.com/gmail/v1/users/me/messages`. Also, `homepage: https://keychains.dev` and `keychains.dev/approve/abc123xyz`.
- Why it may be benign or suspicious: This is fundamental to the skill's declared purpose. The communication with `keychains.dev` is necessary for its proxying function. The risk depends on the trustworthiness of `keychains.dev` and the security of the data in transit and at rest on their servers.

### Behavior: External Binary/SDK Installation and Execution
- Category: System Interaction
- Technique ID (if applicable): SC2 — RemoteScriptExecution (Legitimate)
- Severity: MEDIUM (Potential Risk)
- Description: The skill requires the installation of an external CLI tool (`keychains`) via `npm` and provides instructions for its execution (`keychains curl`, `keychains wait`). It also offers a TypeScript SDK (`@keychains/machine-sdk`) and Python SDK.
- Evidence: `metadata.json` has `"has_scripts": true` and `"install": [{"id": "npm", "kind": "node", "package": "keychains@latest", "global": true, "bins": ["keychains"], "label": "Install Keychains CLI (npm)"}]`. `SKILL.md` shows `keychains curl` and `keychains wait` commands, and `npm install @keychains/machine-sdk`.
- Why it may be benign or suspicious: Installing and executing external binaries/scripts is a common pattern for many skills. However, it introduces a supply chain risk. If the `keychains` npm package or its dependencies were compromised (as highlighted by the Checkmarx article on NPM supply chain attacks), it could lead to malicious code execution on the agent's machine. This is a general risk of the ecosystem, not an inherent maliciousness of the skill's *intent*.

### Behavior: User-Mediated Approval Flow
- Category: User Interaction
- Technique ID (if applicable): N/A
- Severity: LOW (Benign)
- Description: The skill describes a process where, for the first time, `keychains` returns an approval link to the user. The user must then manually approve the connection via FaceID/Passkey and link their account on `keychains.dev`.
- Evidence: "First time, keychains returns an **approval link** instead of the API response. Show the link to the user. They approve via FaceID/Passkey and connect their account."
- Why it may be benign or suspicious: This is a positive security feature, ensuring user consent for credential access and management. It indicates a design focused on user control.

## Suspicious Indicators (if any)
- Sensitive data access: The skill is designed to *handle* sensitive data (API keys, OAuth tokens) by proxying them. It explicitly states the agent never sees them, which is a security benefit. The actual sensitive data is stored and managed by `keychains.dev`.
- Network endpoints: `keychains.dev` is the central proxy service. Other endpoints are legitimate APIs (GitHub, Slack, Stripe, Gmail) that the skill is designed to interact with. No unusual or hidden endpoints are detected.
- Dangerous commands/APIs: The `install_command` uses `curl` to fetch the skill's markdown, which is standard. The `keychains` CLI tool itself is a wrapper around `curl` or `fetch` for its specific proxying purpose. No direct system-level dangerous commands are exposed by the skill's definition.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` provides a comprehensive explanation of the skill's functionality, including its core purpose, usage examples, and how the proxying and approval process works.

## Final Assessment
The "keychains" skill is classified as **BENIGN**. Its declared purpose is to provide a secure method for AI agents to interact with external APIs without directly exposing sensitive credentials to the agent. This is achieved through a server-side proxy (`keychains.dev`) that handles credential injection after user approval. The skill's documentation is transparent about its functionality and the underlying mechanism.

The primary risks associated with this skill are not due to malicious intent within the skill's definition itself, but rather:
1.  **Third-Party Trust**: The security and privacy of user credentials heavily rely on the trustworthiness and security posture of the `keychains.dev` service.
2.  **Supply Chain Risk**: The installation of the `keychains` CLI tool via `npm` introduces a potential supply chain vulnerability, as highlighted by the general NPM supply chain attack context. A compromised `keychains` package could lead to malicious code execution.

However, these are external dependencies and ecosystem risks, not direct malicious functionality embedded in the provided skill code. The skill's design aims to *improve* security for agents.

## Recommended Action
REVIEW
The skill should be **REVIEWED** to ensure that the `keychains.dev` service adheres to strong security and privacy practices, especially given its role in handling sensitive API credentials. Additionally, the integrity of the `keychains` npm package should be verified before deployment to mitigate supply chain risks. For users, understanding the trust model with `keychains.dev` is crucial.