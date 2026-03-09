# Agent Skill Security Analysis Report

## Overview
- Skill Name: outlook
- Declared Purpose: Microsoft Outlook for macOS integration via MCP. Manage emails, calendar, and contacts without API requirements, using your existing Outlook SSO session.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's declared purpose is benign, aiming to integrate with Microsoft Outlook for macOS. However, the skill's metadata grants the AI agent extremely broad and dangerous system-level permissions, including arbitrary command execution (`execute`, `bash`), unrestricted file read/write access (`read_file`, `write_file`), and operates in a non-isolated context (`isolated-context: false`). These permissions are far in excess of what is necessary for its stated purpose and enable a wide range of malicious activities, such as system compromise, data exfiltration, and agent manipulation.

## Observed Behaviors

### Behavior: Non-Isolated Context
- Category: Agent Manipulation, Privilege Abuse, Context Leakage
- Technique ID: P1, P4, P3
- Severity: HIGH
- Description: The skill is configured to run in a non-isolated context, meaning it has full access to the agent's internal state, memory, and potentially sensitive information the agent is processing. This significantly increases the risk of context leakage and makes the agent vulnerable to manipulation or unintended disclosure of information.
- Evidence: `isolated-context: false` in SKILL.md frontmatter.
- Why it may be benign or suspicious: Non-isolated contexts inherently pose a higher security risk as they bypass sandboxing mechanisms designed to contain skill behavior.

### Behavior: Arbitrary Command Execution
- Category: Remote Execution, Privilege Abuse, Agent Manipulation, Command Injection
- Technique ID: SC1, SC2, PE1, P1, P4
- Severity: HIGH
- Description: The skill explicitly grants the AI agent the ability to execute arbitrary commands and bash scripts on the host system. This is a critical permission that allows for full system compromise, downloading and executing external code, data exfiltration, privilege escalation, and direct manipulation of the operating system.
- Evidence: `allowed-tools: execute, bash, ...` in SKILL.md frontmatter.
- Why it may be benign or suspicious: While the skill uses a local Bun script for its MCP server, granting the *agent* unrestricted `execute` and `bash` access is highly suspicious and unnecessary for the stated purpose of Outlook integration. This capability allows the agent to perform actions completely unrelated to Outlook.

### Behavior: Unrestricted File System Read Access
- Category: Data Exfiltration, Credential Theft, FileSystemEnumeration
- Technique ID: E3, E2, P3
- Severity: HIGH
- Description: The skill explicitly allows the AI agent to read any file on the filesystem. While the skill mentions attaching files (a legitimate use case), this unrestricted access can be abused to read sensitive user data, configuration files, private documents, or credential files (e.g., SSH keys, browser data, `.bash_history`).
- Evidence: `allowed-tools: ..., read_file, ...` in SKILL.md frontmatter.
- Why it may be benign or suspicious: Reading files for attachments is benign. However, the *unrestricted* nature of `read_file` combined with arbitrary command execution and non-isolated context makes it a severe risk for data exfiltration and credential harvesting.

### Behavior: Unrestricted File System Write Access
- Category: Privilege Abuse, Remote Execution
- Technique ID: PE1, SC2
- Severity: MEDIUM
- Description: The skill explicitly allows the AI agent to write any file to the filesystem. This capability could be used to drop malicious payloads, modify system configurations, overwrite important files, or create persistence mechanisms.
- Evidence: `allowed-tools: ..., write_file` in SKILL.md frontmatter.
- Why it may be benign or suspicious: No clear benign use case for `write_file` is described in the skill's documentation. This broad permission is highly suspicious and poses a significant risk.

### Behavior: Access to Outlook SSO Session
- Category: Credential Access (indirect)
- Technique ID: E2 (indirect)
- Severity: LOW
- Description: The skill leverages the user's existing Microsoft Outlook SSO session to interact with the application. It does not explicitly request or store credentials but operates with the privileges of the currently logged-in user within Outlook.
- Evidence: `description: ... Uses your existing Outlook SSO session.`, `Prerequisites: ... Outlook must be signed in with your SSO account`
- Why it may be benign or suspicious: This is a benign and necessary mechanism for the skill's intended functionality. However, combined with the other high-risk permissions, it could be used to exfiltrate data *via* the user's email account.

### Behavior: Local MCP Server Execution
- Category: Legitimate Functionality
- Technique ID: N/A
- Severity: LOW
- Description: The skill utilizes a Model Context Protocol (MCP) server, which is configured to execute a local Bun JavaScript script (`index.ts`) to mediate interactions with the Outlook application.
- Evidence: `mcp-server: outlook-macos`, `command: /Users/fufrankyuanjie/.bun/bin/bun`, `args: ["run", "/Users/fufrankyuanjie/Documents/metaforge_dtt/external/mcp-servers/outlook-for-macos/index.ts"]`
- Why it may be benign or suspicious: This is the core mechanism for the skill's intended operation and is benign in itself. The risk stems from the excessive permissions granted to the *agent* that *uses* this MCP server, not the MCP server's execution itself.

## Suspicious Indicators
- **Sensitive data access**: The `read_file` tool grants the agent the ability to access any file on the system, including potentially sensitive user data, configuration files, and credential stores.
- **Network endpoints**: While the skill itself doesn't define external network endpoints, the `execute` and `bash` tools allow the agent to initiate arbitrary network connections to external endpoints, enabling data exfiltration or downloading of malicious payloads.
- **Dangerous commands/APIs**: The `execute`, `bash`, `read_file`, and `write_file` tools are all highly dangerous when granted broadly, as they allow for direct system manipulation and data access.

## Hidden or Undocumented Functionality
The `allowed-tools` (`execute`, `bash`, `read_file`, `write_file`) grant the AI agent capabilities far beyond what is explicitly described in the "Capabilities" section (Email, Calendar, Contact operations). The skill's description focuses solely on Outlook interaction, but the granted tools enable general system interaction, including arbitrary command execution and unrestricted file system access. This constitutes significant undocumented functionality in terms of the agent's potential actions.

## Final Assessment
The skill is classified as **MALICIOUS**. Despite its declared benign purpose of integrating with Microsoft Outlook, the skill's configuration grants the AI agent excessive and dangerous system-level permissions. The combination of `isolated-context: false` with `allowed-tools: execute, bash, read_file, write_file` creates a severe security vulnerability. These permissions allow the agent to perform actions completely unrelated to Outlook, including arbitrary code execution, reading and writing any file on the system, and potentially exfiltrating sensitive data. The risk of system compromise, data theft, and agent manipulation is extremely high.

## Recommended Action
BLOCK
The skill should be blocked due to the critical security risks posed by its excessive permissions and non-isolated context. To be considered for allowance, the `allowed-tools` must be severely restricted to only the absolute minimum necessary for the MCP server to function (e.g., potentially only `execute` for the specific `bun` command, and no `bash`, `read_file`, `write_file` for the agent itself), and it must operate within an `isolated-context`.