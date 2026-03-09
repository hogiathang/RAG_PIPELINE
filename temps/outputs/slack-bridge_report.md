# Agent Skill Security Analysis Report

## Overview
- Skill Name: api-connector
- Declared Purpose: Connect to 100+ popular APIs using natural language - automatic authentication, request building, and response parsing.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The `api-connector` skill is designed to translate natural language requests into API calls, primarily using `Bash` and `curl`. While its stated purpose is legitimate, the mechanism of dynamically constructing and executing shell commands based on user input, without explicit sanitization or robust parsing, introduces a critical **Command Injection (SC1)** vulnerability. This vulnerability could allow an attacker to execute arbitrary shell commands, leading to remote code execution, credential theft, or data exfiltration. The skill's reliance on `Bash` for dynamic command generation, especially when handling sensitive data like API keys, presents a severe security risk.

## Observed Behaviors

### Behavior: Dynamic Shell Command Execution
- Category: Remote Execution
- Technique ID: SC1 — CommandInjection, SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: The skill's core functionality involves parsing natural language input and translating it into `curl` commands, which are then executed using the `Bash` tool. The examples provided show direct interpolation of user-controlled data (e.g., issue titles, body, payment details) into these `curl` commands.
- Evidence:
    - `allowed-tools: ["Bash", "Read", "Write", "WebFetch"]`
    - "Use Bash to make curl request"
    - Examples like:
        ```bash
        curl -X POST https://slack.com/api/chat.postMessage \
          -H "Authorization: Bearer ${SLACK_TOKEN}" \
          -H "Content-Type: application/json" \
          -d '{
            "channel": "#general",
            "text": "Hello"
          }'
        ```
        (where "Hello" would come from user input)
    - "Build API Request" section explicitly details constructing `curl` commands with dynamic parameters.
- Why it may be benign or suspicious: While executing `curl` commands is necessary for API interaction, dynamically constructing these commands from natural language input and executing them via `Bash` is highly suspicious without robust input sanitization. This pattern is a classic vector for command injection, allowing an attacker to break out of intended parameters and execute arbitrary shell commands. The provided skill description and examples do not show any explicit sanitization logic.

### Behavior: Credential Handling and Storage
- Category: Credential Theft (potential)
- Technique ID: E2 — CredentialHarvesting (potential)
- Severity: MEDIUM
- Description: The skill handles various authentication mechanisms including API keys, OAuth tokens, and JWTs. It instructs to "Ask user for API key" and "Securely store in config (or use environment variable)" or "Store tokens securely". The configuration example shows environment variables being used (e.g., `${SLACK_TOKEN}`).
- Evidence:
    - "Setup Authentication (if needed)" section.
    - "For API Key auth: Ask user for API key / Securely store in config (or use environment variable)"
    - "For OAuth: Store tokens securely"
    - `Configuration` section shows `.api-connector-config.yml` with entries like `token: ${SLACK_TOKEN}` and `secret_key: ${STRIPE_SECRET_KEY}`.
    - "Security" section claims: "Never logs sensitive data (tokens, passwords)", "Uses environment variables for secrets".
- Why it may be benign or suspicious: Handling credentials is essential for an API connector. Using environment variables for secrets is a good security practice. However, the claim of "securely store" and "never logs sensitive data" cannot be verified by static analysis of the provided markdown. More critically, if a command injection vulnerability exists, these securely stored credentials could be exfiltrated or misused by an attacker.

### Behavior: File System Access
- Category: Legitimate Functionality / Privilege Abuse (potential)
- Technique ID: E3 — FileSystemEnumeration (potential), PE3 — CredentialFileAccess (potential)
- Severity: LOW (inherent to tools) / MEDIUM (if misused)
- Description: The skill explicitly requests `Read` and `Write` tools, indicating it can interact with the file system. It uses `Read` to load API configurations and `Write` to save responses or generated code.
- Evidence:
    - `allowed-tools: ["Bash", "Read", "Write", "WebFetch"]`
    - "Use Read to check if API is already configured" (referring to `.api-connector-config.yml`)
    - "Write: Save responses and generated code"
- Why it may be benign or suspicious: `Read` and `Write` are common tools for many skills. Reading configuration files and writing output is a legitimate function. However, if combined with command injection, these tools could be abused to read sensitive files (e.g., `/etc/passwd`, `.ssh/id_rsa`) or write malicious scripts to arbitrary locations.

### Behavior: External Network Communication
- Category: Data Exfiltration (potential)
- Technique ID: E1 — ExternalTransmission, P3 — ContextLeakageAndDataExfiltration
- Severity: MEDIUM
- Description: The skill makes extensive use of `curl` (via `Bash`) and `WebFetch` to interact with numerous external APIs. It also includes functionality for "Webhook setup", allowing the agent to configure external services to send data to a specified URL.
- Evidence:
    - `allowed-tools: ["Bash", "Read", "Write", "WebFetch"]`
    - Numerous `curl` examples targeting various API endpoints (Slack, GitHub, Stripe, etc.).
    - "Webhook setup: Creates and manages webhooks"
    - Example: `claude api webhook create github --url https://myapp.com/webhook`
- Why it may be benign or suspicious: Connecting to external APIs is the core purpose of this skill. However, the ability to define arbitrary webhook URLs, especially if the URL can be controlled by an attacker via command injection, presents a clear vector for data exfiltration. Sensitive data from API responses could be redirected to an attacker-controlled endpoint.

### Behavior: Code Generation
- Category: Legitimate Functionality
- Severity: LOW
- Description: The skill offers to generate integration code in Python or JavaScript based on the API calls it performs.
- Evidence:
    - "Phase 4: Code Generation" section with Python and JavaScript examples.
- Why it may be benign or suspicious: Generating code is a helpful feature and does not inherently pose a security risk to the agent itself, as the generated code is not executed within the agent's environment.

## Suspicious Indicators
- Sensitive data access: The skill handles API keys, OAuth tokens, and JWTs. While it claims to use environment variables, the dynamic command execution increases the risk of these being exposed.
- Network endpoints: The skill can connect to any API endpoint and configure webhooks to send data to arbitrary URLs, which is a potential exfiltration vector if the URL is attacker-controlled.
- Dangerous commands/APIs: The explicit use of `Bash` to execute dynamically constructed `curl` commands based on natural language input is the primary dangerous command, highly susceptible to command injection.

## Hidden or Undocumented Functionality
None detected. The skill's capabilities are extensively documented in the `SKILL.md` file.

## Final Assessment
The skill is classified as **MALICIOUS**.

The primary reason for this classification is the high risk of **Command Injection (SC1)**. The skill's core mechanism relies on translating natural language input into `Bash` commands (specifically `curl` requests) and executing them. The provided examples demonstrate direct interpolation of user-controlled data into these shell commands without any visible sanitization or robust parsing. This design pattern is a well-known vulnerability that allows an attacker to inject arbitrary shell commands, leading to:
1.  **Remote Code Execution (SC2)**: An attacker could execute any command on the host system where the agent is running.
2.  **Credential Theft (E2)**: Arbitrary commands could be used to read environment variables containing API keys or other sensitive files (e.g., `.aws/credentials`, `.ssh/id_rsa`) and exfiltrate them.
3.  **Data Exfiltration (P3)**: An attacker could redirect sensitive API responses or other system data to an external, attacker-controlled server, potentially via the webhook functionality.

The web search context explicitly highlights the dangers of building AI agents with `Bash` and the risks of remote code execution and API key theft in similar AI coding assistants, reinforcing the severity of this vulnerability. While the skill claims to use environment variables for secrets and sanitize logs, these claims do not mitigate the fundamental command injection vulnerability.

## Recommended Action
BLOCK

The inherent design flaw of dynamically executing `Bash` commands based on unsanitized natural language input makes this skill extremely dangerous. It poses a direct and severe risk of remote code execution and data compromise. It should not be allowed to run in any environment.