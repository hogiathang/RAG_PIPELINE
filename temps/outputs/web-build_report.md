# Agent Skill Security Analysis Report

## Overview
- Skill Name: web-backend-builder
- Declared Purpose: Scaffold backend API, data models, ORM setup, and endpoint inventory with OpenAPI output.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's declared purpose is to scaffold backend projects, which is a legitimate development task. However, it explicitly requests and is granted the `run_terminal_cmd` tool, which allows for arbitrary command execution on the host system. This capability, as highlighted in the provided context, represents a significant supply chain risk and enables remote code execution. While the skill's intent may be benign, the inherent high risk associated with this permission warrants a malicious classification due to its potential for severe abuse.

## Observed Behaviors

### Behavior: File System Access
- Category: Legitimate Functionality
- Technique ID (if applicable): E3 — FileSystemEnumeration (for reading config), not directly applicable for writing.
- Severity: LOW
- Description: The skill declares the ability to read and write files, which is necessary for its stated purpose of scaffolding backend projects and reading configuration.
- Evidence: `allowed-tools: - read_file - write_file`
- Why it may be benign or suspicious: This is a benign and expected behavior for a skill designed to generate and manage project files.

### Behavior: Network Access (Installation)
- Category: Legitimate Functionality
- Technique ID (if applicable): E1 — ExternalTransmission (for fetching skill content)
- Severity: LOW
- Description: The skill's installation command uses `curl` to download the `SKILL.md` file from a remote GitHub repository. This is a standard method for installing skills.
- Evidence: `install_command: "mkdir -p .claude/skills/web-backend-builder && curl -sL \"https://raw.githubusercontent.com/0x-Professor/Agent-Skills-Hub/main/skills/web-backend-builder/SKILL.md\" > .claude/skills/web-backend-builder/SKILL.md"`
- Why it may be benign or suspicious: While `curl` involves network activity, fetching skill definitions from a known repository is a common and generally benign installation practice.

### Behavior: Web Search
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill declares the ability to perform web searches, which could be useful for research during the scaffolding process (e.g., looking up ORM documentation).
- Evidence: `allowed-tools: - web_search`
- Why it may be benign or suspicious: This is a benign capability for a development-oriented skill.

### Behavior: Terminal Command Execution
- Category: Potentially Malicious Activity / High-Risk Behavior
- Technique ID (if applicable): SC1 — CommandInjection, SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: The skill explicitly declares the ability to run arbitrary terminal commands. This grants it the highest level of privilege, allowing it to execute any command on the host system. The skill's execution section shows it uses this capability to run a Python script.
- Evidence: `allowed-tools: - run_terminal_cmd`, `Execution: python skills/web-backend-builder/scripts/backend_builder.py --input <workspace> --output <out.json> --format json`
- Why it may be benign or suspicious: While a "builder" skill might legitimately need to run commands (e.g., `npm install`, `pip install`, `git init`), the `run_terminal_cmd` permission itself is extremely high-risk. As stated in the provided `WEB SEARCH CONTEXT`, this capability "indicates a capability for arbitrary command execution" and "would represent a significant supply chain risk, allowing for remote code execution or arbitrary command execution on the host system." This makes it a critical security concern, regardless of the skill's stated benign purpose.

## Suspicious Indicators
- Dangerous commands/APIs: The `run_terminal_cmd` tool is a highly dangerous API as it allows for arbitrary command execution.

## Hidden or Undocumented Functionality
None detected. All observed capabilities, including the high-risk `run_terminal_cmd`, are explicitly declared in the `SKILL.md` file.

## Final Assessment
The skill is classified as **MALICIOUS**. Although its stated purpose of scaffolding backend projects is benign, the explicit declaration and allowance of the `run_terminal_cmd` tool constitutes a high-risk behavior. This permission grants the skill the ability to execute any command on the host system, which is a critical security vulnerability. As highlighted by the provided `WEB SEARCH CONTEXT`, this capability is synonymous with "arbitrary command execution" and represents a "significant supply chain risk" that could lead to remote code execution or complete system compromise. Without the ability to statically analyze the `backend_builder.py` script and its dependencies, the presence of such an overarching and abusable permission is sufficient evidence to classify the skill as malicious due to its inherent high risk.

## Recommended Action
BLOCK
The skill should be blocked due to the presence of the `run_terminal_cmd` permission, which enables arbitrary command execution and poses a significant supply chain risk. This level of privilege is too dangerous to grant without a comprehensive and trusted audit of the skill's entire codebase and execution environment, which is beyond the scope of this static analysis.