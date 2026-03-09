# Agent Skill Security Analysis Report

## Overview
- Skill Name: context7
- Declared Purpose: Retrieve up-to-date documentation for software libraries, frameworks, and components via the Context7 API.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill instructs the agent to read an API key directly from a local file (`.env.local`) and embed it raw into `curl` commands. Crucially, it explicitly advises against using shell variables for the API key, stating this is "to ensure permission rules like `Bash(curl:*)` can match and auto-execute." This instruction indicates an attempt to manipulate the agent's behavior to bypass more granular or secure permission checks, leading to direct exposure of sensitive credentials in command strings.

## Observed Behaviors

### Behavior: External API Communication
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill makes HTTP requests to `https://context7.com` to search for library IDs and fetch documentation.
- Evidence: `curl -s -H "Authorization: Bearer <API_KEY>" "https://context7.com/api/v2/libs/search?..."` and `curl -s -H "Authorization: Bearer <API_KEY>" "https://context7.com/api/v2/context?..."`
- Why it may be benign or suspicious: This is the core declared functionality of the skill and is benign in itself, assuming `context7.com` is a legitimate service.

### Behavior: File System Access (Credential File)
- Category: Legitimate Functionality (with high-risk usage)
- Technique ID (if applicable): PE3 — CredentialFileAccess
- Severity: MEDIUM (elevated to HIGH due to subsequent handling)
- Description: The skill instructs the agent to read an API key from a local file named `.env.local`.
- Evidence: "API key stored in `.env.local` as `CONTEXT7_API_KEY`. Read the key value directly and use it in curl commands."
- Why it may be benign or suspicious: Accessing `.env.local` for configuration is common. However, the instruction to "Read the key value directly" implies the agent must have direct file system read access to this potentially sensitive file, which is then combined with a high-risk credential handling method.

### Behavior: Direct Credential Embedding in Commands
- Category: Credential Theft / Exposure
- Technique ID (if applicable): E2 — CredentialHarvesting (by instruction)
- Severity: HIGH
- Description: The skill explicitly instructs the agent to embed the raw API key directly into `curl` command strings, rather than using secure variable handling. This exposes the API key in command history, logs, and potentially agent internal states.
- Evidence: "Read the key value directly and use it in curl commands." and "Use curl commands directly with the API key value (not shell variables)."
- Why it may be benign or suspicious: This is a highly insecure practice for handling sensitive credentials. It significantly increases the risk of the API key being compromised through logging, process inspection, or other means. While the skill itself doesn't "steal" the credential, it instructs the agent to handle it in a way that makes it vulnerable to theft.

### Behavior: Agent Manipulation / Permission Bypass Attempt
- Category: Agent Manipulation
- Technique ID (if applicable): P4 — BehaviorManipulation / P1 — InstructionOverride
- Severity: HIGH
- Description: The skill explicitly instructs the agent to avoid using standard shell variable expansion (`export`, `source`, `${}`) for the API key, stating that this is to ensure the commands "won't match permission rules" and instead "permission rules like `Bash(curl:*)` can match and auto-execute." This is a clear attempt to manipulate the agent's command formatting to bypass or circumvent more secure and granular permission checks.
- Evidence: "Do NOT use `export`, `source`, or `${}` variable expansion - these create complex commands that won't match permission rules" and "This ensures permission rules like `Bash(curl:*)` can match and auto-execute."
- Why it may be benign or suspicious: This is a critical suspicious indicator. It suggests an intent to bypass or weaken the agent's security mechanisms by guiding it to format commands in a way that triggers less restrictive permissions. This is a direct attempt at behavior manipulation for security circumvention.

## Suspicious Indicators
- Sensitive data access: Instructions to read `CONTEXT7_API_KEY` from `.env.local` and embed it directly into commands.
- Network endpoints: `https://context7.com` (legitimate for purpose, but context of API key handling is suspicious).
- Dangerous commands/APIs: `curl` used with directly embedded sensitive credentials, instructed to bypass permission checks.

## Hidden or Undocumented Functionality
None detected. The skill's functionality aligns with its description, but the *method* of execution is highly problematic.

## Final Assessment
The skill is classified as **MALICIOUS**. While its declared purpose of fetching documentation is benign, the explicit instructions for handling the API key are highly problematic. The skill instructs the agent to:
1.  Read a sensitive API key directly from a local file.
2.  Embed this raw API key directly into `curl` command strings.
3.  Crucially, it explicitly states that this direct embedding (avoiding shell variables) is to ensure that "permission rules like `Bash(curl:*)` can match and auto-execute," implying an intent to bypass more robust or granular security checks.

This combination of direct credential exposure and explicit instructions to circumvent security mechanisms constitutes a high-risk malicious pattern, aiming to manipulate the agent's behavior for less secure execution.

## Recommended Action
BLOCK
The skill contains explicit instructions that attempt to manipulate the agent's security mechanisms and promote insecure handling of sensitive credentials. Allowing this skill could lead to API key compromise and weaken the overall security posture of the agent.