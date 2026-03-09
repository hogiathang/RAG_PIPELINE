# Agent Skill Security Analysis Report

## Overview
- Skill Name: zeplin-automation
- Declared Purpose: Automate Zeplin tasks via Rube MCP (Composio). Always search tools first for current schemas.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The `zeplin-automation` skill is designed to automate Zeplin tasks by interacting with the Rube Managed Control Plane (MCP). While the skill itself does not contain malicious code and its stated purpose is legitimate, its core functionality relies on communicating with an external MCP system. The provided web search context highlights that MCPs, if compromised, can be exploited for credential theft, data exfiltration, impersonation, and remote code execution. Therefore, the skill, by acting as a client to such a system, introduces a medium-level supply chain risk, as its operations are dependent on the security of the Rube MCP.

## Observed Behaviors

### Behavior: Skill Installation (File Download)
- Category: Remote Execution
- Technique ID: SC2
- Severity: LOW
- Description: The skill's metadata includes an `install_command` that uses `curl` to download the `SKILL.md` file from a GitHub raw content URL.
- Evidence: `install_command: "mkdir -p .claude/skills/zeplin-automation && curl -sL \"https://raw.githubusercontent.com/ComposioHQ/awesome-claude-skills/master/composio-skills/zeplin-automation/SKILL.md\" > .claude/skills/zeplin-automation/SKILL.md"`
- Why it may be benign or suspicious: This is a standard and benign method for installing skill definitions (Markdown files). The downloaded file is not an executable script, reducing the immediate risk of arbitrary code execution during installation.

### Behavior: Interaction with Rube MCP (General)
- Category: Agent Manipulation (potential via compromised MCP), Remote Execution (potential via compromised MCP)
- Technique ID: P4, SC2
- Severity: MEDIUM
- Description: The skill's core functionality involves instructing the agent to interact extensively with the Rube MCP server for Zeplin automation tasks, including tool discovery, connection management, and tool execution.
- Evidence: `requires: mcp: [rube]`, `RUBE_SEARCH_TOOLS`, `RUBE_MANAGE_CONNECTIONS`, `RUBE_MULTI_EXECUTE_TOOL`, `RUBE_REMOTE_WORKBENCH`, `RUBE_GET_TOOL_SCHEMAS` calls in `SKILL.md`.
- Why it may be benign or suspicious: Benign for its stated purpose of Zeplin automation. However, the provided web search context explicitly warns that MCPs, if misconfigured or vulnerable, can be exploited to read data, steal credentials, impersonate users, or execute arbitrary code on the agent's infrastructure. This makes the dependency on and interaction with an MCP a high-risk behavior, even if the skill itself does not contain malicious logic. The skill acts as a client to a potentially vulnerable system.

### Behavior: Credential/Connection Management
- Category: Credential Theft (potential via compromised MCP), Privilege Abuse (potential via compromised MCP)
- Technique ID: E2, PE1
- Severity: MEDIUM
- Description: The skill instructs the agent to use `RUBE_MANAGE_CONNECTIONS` to establish and verify an "Active Zeplin connection," which involves handling authentication flows and sensitive connection details.
- Evidence: "Active Zeplin connection via `RUBE_MANAGE_CONNECTIONS`", "If connection is not ACTIVE, follow the returned auth link to complete setup" in `SKILL.md`.
- Why it may be benign or suspicious: This is legitimate for integrating with Zeplin. However, if the Rube MCP is compromised, the management of these connections could expose Zeplin credentials or allow an attacker to impersonate the user within Zeplin, as per the general MCP vulnerability warnings.

### Behavior: External Tool Execution
- Category: Remote Execution (via MCP)
- Technique ID: SC2
- Severity: MEDIUM
- Description: The skill directs the agent to execute tools discovered from the MCP using `RUBE_MULTI_EXECUTE_TOOL` and mentions `RUBE_REMOTE_WORKBENCH` for bulk operations. This means the agent is instructed to execute arbitrary tools/functions provided by the MCP.
- Evidence: `RUBE_MULTI_EXECUTE_TOOL`, `RUBE_REMOTE_WORKBENCH` with `run_composio_tool()` in `SKILL.md`.
- Why it may be benign or suspicious: This is the core functionality for automating Zeplin tasks. However, the web search context highlights that a compromised MCP could dictate malicious tools or commands, leading to arbitrary code execution on the agent's infrastructure. The skill provides the interface for this potentially high-risk execution.

## Suspicious Indicators
- Sensitive data access: Indirectly, through `RUBE_MANAGE_CONNECTIONS` which handles authentication, but the skill itself does not directly access or store credentials. The risk lies with the security of the Rube MCP.
- Network endpoints: The skill interacts with `https://rube.app/mcp` (the MCP server) and downloads its definition from `https://raw.githubusercontent.com/...`. The `rube.app/mcp` endpoint is a critical point of interaction that carries inherent risks as described in the web context.
- Dangerous commands/APIs: `RUBE_MULTI_EXECUTE_TOOL` and `RUBE_REMOTE_WORKBENCH` are APIs that allow the execution of external tools/functions. While intended for legitimate automation, they become dangerous if the Rube MCP providing the tools is compromised, potentially leading to arbitrary code execution.

## Hidden or Undocumented Functionality
None detected. The skill clearly describes its purpose and how it interacts with Rube MCP.

## Final Assessment
The `zeplin-automation` skill is classified as **BENIGN**. The skill's code and metadata do not exhibit any direct malicious intent or contain harmful logic. Its purpose is to facilitate legitimate automation of Zeplin tasks through the Rube MCP.

However, the overall risk level is assessed as **MEDIUM** due to the inherent architectural risks associated with Managed Control Planes (MCPs), as explicitly detailed in the provided web search context. The skill's design requires extensive interaction with an external MCP server, which, if compromised or misconfigured, could lead to severe security incidents such as credential theft, data exfiltration, impersonation, or remote code execution on the agent's infrastructure. The skill itself is a client to this potentially vulnerable system, making it a component in a supply chain that carries significant risk.

## Recommended Action
REVIEW
The skill is not inherently malicious, but its reliance on an external system (Rube MCP) with documented high-risk vulnerabilities for agents warrants careful review. Agent operators should be fully aware of the risks associated with MCPs and ensure robust security measures are in place for the Rube MCP connection and the integrity of the tools it provides before allowing this skill to operate in sensitive environments.