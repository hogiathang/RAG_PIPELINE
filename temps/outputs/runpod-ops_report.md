# Agent Skill Security Analysis Report

## Overview
- Skill Name: runpod-ops
- Declared Purpose: Provision, manage, and terminate RunPod GPU instances for LLM training.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The `runpod-ops` skill is designed to manage RunPod GPU instances using `Bash` commands and requires a `RUNPOD_API_KEY`. It is described as "self-contained" and "auto-installs via `uv run` from git," meaning it dynamically fetches and executes its core logic from a GitHub repository. While its declared purpose is legitimate, the dynamic code loading and execution, coupled with the requirement for a sensitive API key, introduce a medium level of risk. There is no direct evidence of malicious intent, but the full scope of its behavior cannot be statically analyzed without the fetched `run.sh` script.

## Observed Behaviors

### Behavior: External Command Execution
- Category: Remote Execution
- Technique ID: SC2 — RemoteScriptExecution
- Severity: MEDIUM
- Description: The skill explicitly uses the `Bash` tool to execute a local shell script (`.agents/skills/runpod-ops/run.sh`) with various arguments to perform RunPod management operations (e.g., create, list, monitor, terminate instances).
- Evidence: `allowed-tools: Bash`, examples like `.agents/skills/runpod-ops/run.sh create-instance 70B --hours 4`.
- Why it may be benign or suspicious: This is benign as it's the core functionality for managing cloud resources. It is suspicious because it relies on an external script (`run.sh`) whose full content is not provided in this static analysis, and which is dynamically fetched (see "Dynamic Code Loading" below).

### Behavior: Credential Requirement
- Category: Credential Management
- Technique ID: None directly applicable for theft by the skill, but involves sensitive data.
- Severity: LOW (for the skill's direct action), MEDIUM (for the overall risk of the agent handling it).
- Description: The skill requires the `RUNPOD_API_KEY` environment variable for authenticating with the RunPod API.
- Evidence: "Environment Variables | `RUNPOD_API_KEY` | Yes | RunPod API key".
- Why it may be benign or suspicious: Benign as it's a necessary credential for legitimate API interaction with RunPod. Suspicious because API keys are highly sensitive and grant significant control over cloud resources, making the agent a high-value target if compromised. The skill itself does not appear to exfiltrate this key.

### Behavior: Dynamic Code Loading/Execution (Self-Installation)
- Category: Remote Execution, Hidden Functionality
- Technique ID: SC2 — RemoteScriptExecution, P2 — HiddenInstructions
- Severity: MEDIUM
- Description: The skill is described as "self-contained" and "auto-installs via `uv run` from git." This indicates that the agent is instructed to fetch and execute code from a remote GitHub repository (`github.com/grahama1970/agent-skills`) to set up the skill's operational logic.
- Evidence: "Self-contained skill - auto-installs via `uv run` from git (no pre-installation needed)."
- Why it may be benign or suspicious: Benign as it's a declared mechanism for self-contained skills to manage their own setup. Suspicious because it involves dynamic fetching and execution of code from an external source, which introduces a supply chain risk. The full logic of the skill (contained within the `run.sh` script and its dependencies) is not available for static analysis, creating a potential blind spot for security review.

### Behavior: Filesystem Read Access
- Category: FileSystemEnumeration (potential)
- Technique ID: E3 — FileSystemEnumeration (potential)
- Severity: LOW
- Description: The `Read` tool is explicitly allowed for the skill.
- Evidence: `allowed-tools: Read`.
- Why it may be benign or suspicious: Benign for legitimate purposes like reading configuration files or logs. No evidence of misuse for enumerating or exfiltrating sensitive files is present in the provided `SKILL.md`.

### Behavior: External API Interaction
- Category: External Transmission
- Technique ID: E1 — ExternalTransmission
- Severity: LOW
- Description: The skill interacts with the RunPod API to provision, manage, and terminate GPU instances.
- Evidence: "Provision, manage, and terminate RunPod GPU instances".
- Why it may be benign or suspicious: Benign as it's the core declared purpose of the skill to interact with the RunPod service.

## Suspicious Indicators
- Sensitive data access: The skill requires `RUNPOD_API_KEY`, a highly sensitive credential.
- Network endpoints: Interacts with the RunPod API (legitimate). Fetches code from `github.com/grahama1970/agent-skills` for self-installation, which is a declared but powerful network operation.
- Dangerous commands/APIs: The `Bash` tool is allowed, and the skill instructs the agent to execute `uv run` from git, which is a powerful command for dynamic code loading and execution.

## Hidden or Undocumented Functionality
The "auto-installs via `uv run` from git" mechanism means that the actual executable logic of the skill (the `run.sh` script and any associated dependencies) is fetched and executed dynamically from a remote source. While this mechanism is mentioned, the full implications of this dynamic loading are not detailed, and the content of `run.sh` is not provided for static analysis. This makes the complete scope of the skill's capabilities opaque without further investigation of the remote repository's contents.

## Final Assessment
The skill is classified as **BENIGN**. Its declared purpose of managing RunPod GPU instances is legitimate, and the observed behaviors, including the use of `Bash` and interaction with external APIs, are consistent with this purpose. There is no direct evidence of malicious intent such as credential theft, data exfiltration to undeclared endpoints, or privilege abuse beyond what is necessary for its function.

However, the skill carries a **MEDIUM** overall risk due to two main factors:
1.  **Dynamic Code Loading**: The "auto-installs via `uv run` from git" mechanism means the skill's core logic is fetched and executed dynamically from an external GitHub repository. While this is a declared feature for "self-contained" skills, it introduces a supply chain risk. If the GitHub repository were compromised, malicious code could be injected and executed by the agent without prior static analysis of the full skill logic.
2.  **Sensitive Credential Handling**: The skill requires a `RUNPOD_API_KEY`, which grants significant control over cloud resources. While the skill itself doesn't appear to misuse this key, its presence makes the agent a higher-value target for attackers.

## Recommended Action
**REVIEW**

The dynamic code loading from GitHub means that the actual executable logic (`run.sh` and its dependencies) is not part of this static analysis. A thorough review of the `run.sh` script and the entire contents of the `grahama1970/agent-skills` repository at the specified path (`skills/runpod-ops`) is necessary to fully ascertain the skill's safety and ensure no malicious code is present or could be introduced via a supply chain attack. The handling and storage of the `RUNPOD_API_KEY` by the agent should also be carefully considered.