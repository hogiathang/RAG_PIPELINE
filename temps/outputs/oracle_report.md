# Agent Skill Security Analysis Report

## Overview
- Skill Name: oracle
- Declared Purpose: Best practices for using the oracle CLI (prompt + file bundling, engines, sessions, and file attachment patterns). It bundles user prompts and selected files into a "one-shot" request for AI models (API or browser automation) to provide context-aware answers.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The `oracle` skill provides a CLI tool for interacting with AI models by bundling user-specified files and prompts. Its core functionalities involve reading local files, communicating with external AI APIs or browser automation, and managing sessions. The skill explicitly advises users on handling sensitive data and includes features to limit file exposure. All observed behaviors are consistent with its declared purpose and do not show signs of malicious intent.

## Observed Behaviors

### Behavior: File System Access (Read)
- Category: FileSystemEnumeration
- Technique ID: E3
- Severity: LOW
- Description: The skill reads files and directories specified by the user via the `--file` argument, supporting globs and exclusions. It also respects `.gitignore` and has default ignored directories (e.g., `node_modules`, `.git`). It filters dotfiles and rejects files larger than 1 MB.
- Evidence: "Attaching files (`--file`)", "Include: `--file "src/**"`", "Exclude: `--file "src/**" --file "!src/**/*.test.ts"`", "Defaults (implementation behavior): Honors `.gitignore`... Files > 1 MB rejected."
- Why it may be benign or suspicious: This is a core, legitimate function of the tool, as its purpose is to bundle files with prompts. The exclusion rules, `.gitignore` honoring, and file size limits are positive security practices to prevent accidental oversharing.

### Behavior: File System Access (Write/Storage)
- Category: Data Storage
- Technique ID: N/A
- Severity: LOW
- Description: The skill stores session data in `~/.oracle/sessions`.
- Evidence: "Sessions + slugs: Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`)."
- Why it may be benign or suspicious: This is standard behavior for CLI tools that manage persistent sessions or state. The location is within the user's home directory, which is appropriate.

### Behavior: External Network Communication
- Category: ExternalTransmission
- Technique ID: E1
- Severity: LOW
- Description: The skill communicates with external AI models via API (`--engine api`) or browser automation (`--engine browser`). It can also start a local server (`oracle serve`) to accept remote connections, and a client can connect to a remote host (`--remote-host`).
- Evidence: "Engines (API vs browser)", "Auto-pick: `api` when `OPENAI_API_KEY` is set; otherwise `browser`.", "Remote browser host: `oracle serve --host 0.0.0.0 --port 9473 --token <secret>`", "Client: `oracle --engine browser --remote-host <host:port> --remote-token <secret>`"
- Why it may be benign or suspicious: This is fundamental to the skill's purpose of interacting with AI models. The `oracle serve` command explicitly creates a network listener, which is a feature, not an exploit, and requires a token for authentication.

### Behavior: Credential Usage
- Category: CredentialHarvesting (but benign use)
- Technique ID: E2 (used for legitimate purpose, not harvesting)
- Severity: LOW
- Description: The skill uses the `OPENAI_API_KEY` environment variable for API access and requires `--token` arguments for its `serve` and `remote-host` functionalities. It explicitly warns users about attaching secrets.
- Evidence: "Auto-pick: `api` when `OPENAI_API_KEY` is set", "`oracle serve --host 0.0.0.0 --port 9473 --token <secret>`", "Client: `oracle --engine browser --remote-host <host:port> --remote-token <secret>`", "Safety: Don’t attach secrets by default (`.env`, key files, auth tokens). Redact aggressively; share only what’s required."
- Why it may be benign or suspicious: The skill uses credentials provided by the user for its intended functionality. The explicit safety warning demonstrates awareness of the risks associated with sensitive data and advises users on best practices, which is a strong indicator of benign intent. There is no evidence of the skill attempting to *harvest* or exfiltrate credentials without user consent.

### Behavior: Package Execution
- Category: RemoteScriptExecution (but benign use)
- Technique ID: SC2 (used for package management, not arbitrary script execution)
- Severity: LOW
- Description: The skill's documentation suggests using `npx -y @steipete/oracle --help` to run the binary if not installed. `npx` is a Node.js package runner that can download and execute packages.
- Evidence: "If the binary isn’t installed: `npx -y @steipete/oracle --help`"
- Why it may be benign or suspicious: `npx` is a standard and common tool in the Node.js ecosystem for executing CLI tools without global installation. It executes a known, specified package (`@steipete/oracle`), not arbitrary or unknown code. This is a benign use of a package manager utility.

## Suspicious Indicators
- Sensitive data access: The skill uses `OPENAI_API_KEY` and custom tokens for its operation. However, this is necessary for its stated purpose, and the skill explicitly warns users about handling secrets.
- Network endpoints: The skill connects to external AI APIs and can optionally start a local server (`oracle serve`). These are core functionalities and are explicitly documented.
- Dangerous commands/APIs: None identified as dangerous outside of their intended, documented use.

## Hidden or Undocumented Functionality
- `--copy` is an alias for `--copy-markdown`. This is explicitly noted in the documentation ("Note: `--copy` is a hidden alias for `--copy-markdown`."), so it's not truly hidden functionality in a malicious sense.
- None detected beyond the above.

## Final Assessment
The `oracle` skill is classified as **BENIGN**. The static analysis reveals that all its functionalities, including file system access, network communication, and credential usage, are directly aligned with its declared purpose of bundling prompts and files for AI model interaction. The skill incorporates several positive security practices, such as respecting `.gitignore`, filtering files by type/size, and providing explicit safety warnings regarding sensitive data. There is no evidence of credential theft, unauthorized data exfiltration, arbitrary remote code execution, privilege abuse, or malicious hidden functionality. The use of `npx` and the ability to start a local server are standard and documented features for CLI tools.

## Recommended Action
ALLOW
The skill's functionality is transparent, well-documented, and includes user-centric safety advice. Its behaviors are consistent with a legitimate development tool.