# Agent Skill Security Analysis Report

## Overview
- Skill Name: cloud-common
- Declared Purpose: Shared utilities for faber-cloud plugin - configuration loading, pattern resolution, auto-discovery
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The `cloud-common` skill provides essential utilities for cloud infrastructure management, including configuration loading, pattern substitution, and auto-discovery of project and cloud provider details. It explicitly allows `Bash` and `Read` tools to perform these operations, which involve filesystem access (reading/writing configuration files, interacting with Git repositories) and access to AWS credentials for auto-discovery of the AWS account ID. While accessing AWS credentials is a sensitive operation, it is a common and often necessary function for cloud management tools and is explicitly declared as part of its auto-discovery mechanism. There is no evidence of credential exfiltration or other malicious activities. The skill's operations are well-documented and align with its stated purpose.

## Observed Behaviors

### Behavior: Configuration File Access and Management
- Category: Filesystem Interaction
- Technique ID (if applicable): E3 — FileSystemEnumeration
- Severity: LOW
- Description: The skill reads configuration from `.fractary/plugins/faber-cloud/config.json`, `faber-cloud.json`, and `devops.json` in the project working directory. It also performs automatic migration by renaming `faber-cloud.json` to `config.json`.
- Evidence: "Configuration loading from `.fractary/plugins/faber-cloud/config.json`", "Backward compatibility with `faber-cloud.json` and `devops.json`", "If `faber-cloud.json` exists: automatically rename to `config.json`"
- Why it may be benign or suspicious: This is a legitimate function for a configuration management utility. Renaming files for backward compatibility is a common practice in software updates. The explicit instruction to load from the "project working directory" rather than the plugin installation directory is a good security practice, limiting its scope.

### Behavior: Bash Script Execution
- Category: Local Execution
- Technique ID (if applicable): SC1 — CommandInjection (potential, but not directly observed)
- Severity: MEDIUM
- Description: The skill is designed to source and execute a Bash script (`scripts/config-loader.sh`) to perform its core functions.
- Evidence: `allowed-tools: Bash`, "source "${SKILL_DIR}/../cloud-common/scripts/config-loader.sh""
- Why it may be benign or suspicious: Allowing `Bash` is necessary for a utility script that performs system-level operations like file management and environment variable manipulation. The risk is inherent in any `Bash` execution, as it grants the agent significant control over the local environment. However, for a utility skill, this is expected. Without the actual script content, we assume it performs only the described actions.

### Behavior: Git Repository Interaction
- Category: Filesystem Interaction, Information Gathering
- Technique ID (if applicable): E3 — FileSystemEnumeration
- Severity: LOW
- Description: The skill auto-discovers project name and organization from the Git repository and its remotes. This implies executing `git` commands.
- Evidence: "Project name from Git repository", "Organization from Git remote"
- Why it may be benign or suspicious: This is a common and legitimate way for development tools to infer project context. It involves reading local `.git` directories and potentially querying remote repositories (which might involve network requests, but for information gathering, not exfiltration).

### Behavior: AWS Credential Access for Account ID Discovery
- Category: Credential Theft (Access)
- Technique ID (if applicable): E2 — CredentialHarvesting, PE3 — CredentialFileAccess
- Severity: HIGH
- Description: The skill attempts to auto-discover the AWS account ID by accessing AWS credentials.
- Evidence: "AWS account ID from credentials"
- Why it may be benign or suspicious: For a cloud management skill, accessing AWS credentials to identify the current account context is a necessary and legitimate function. However, any interaction with credentials carries inherent risk. The description states it gets the "account ID," not the raw credentials for exfiltration. Without the actual script, we cannot confirm the exact method or scope of access. This is classified as HIGH severity due to the sensitive nature of credential access, even if the stated purpose is benign.

### Behavior: Pattern Substitution
- Category: Data Processing
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill provides functionality to substitute placeholders (e.g., `{project}`, `{environment}`) in patterns.
- Evidence: "Pattern substitution (`{project}`, `{environment}`, etc.)", "resolve_pattern(pattern, environment)"
- Why it may be benign or suspicious: This is a benign string manipulation utility, common in configuration management.

## Suspicious Indicators (if any)
- Sensitive data access: Explicit access to "AWS account ID from credentials".
- Network endpoints: Implied network access for "Organization from Git remote" (to fetch remote details) and potentially for AWS credential validation/discovery (e.g., `aws sts get-caller-identity`). These are for legitimate discovery purposes.
- Dangerous commands/APIs: The use of `Bash` allows for arbitrary command execution. However, the described functions (file operations, Git commands, AWS CLI commands) are standard for this type of utility.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` provides a comprehensive description of the skill's purpose and components, including specific functions and variables.

## Final Assessment
The skill is classified as **BENIGN**. While it performs sensitive operations such as accessing AWS credentials and executing Bash scripts, these actions are explicitly declared and align with the stated purpose of a "Shared utilities for faber-cloud plugin - configuration loading, pattern resolution, auto-discovery" for cloud infrastructure management. The skill's documentation emphasizes loading configuration from the project working directory, which is a good security practice. There is no evidence of data exfiltration, remote code execution, privilege abuse, or hidden malicious functionality. The risk associated with credential access is acknowledged, but it appears to be for a legitimate operational purpose within the context of a cloud management tool.

## Recommended Action
REVIEW
The skill's access to AWS credentials, while declared and potentially benign, warrants a review of the actual `config-loader.sh` script to confirm that credential access is limited to retrieving the account ID and not broader harvesting or exfiltration. If the script's implementation aligns with the stated benign purpose, the skill can be allowed.