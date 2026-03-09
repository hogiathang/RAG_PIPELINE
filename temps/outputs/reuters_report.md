# Agent Skill Security Analysis Report

## Overview
- Skill Name: Gemini Web Search (as per SKILL.md) / Router (as per metadata.json)
- Declared Purpose: Use Gemini CLI to perform web searches, fact-finding, and return a sourced summary.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's primary function is to execute the Gemini CLI for web searches. However, it explicitly instructs the agent to construct shell commands by directly embedding user-provided prompts without any apparent sanitization. This design introduces a severe command injection vulnerability (SC1), allowing for arbitrary command execution if the calling agent does not rigorously sanitize input. While the skill's stated purpose is benign, its implementation creates a high-risk attack vector.

## Observed Behaviors

### Behavior: Command Execution with Unsanitized Input
- Category: Remote Execution / Agent Manipulation
- Technique ID: SC1 — CommandInjection
- Severity: HIGH
- Description: The skill provides templates for executing the `gemini` CLI using `functions.exec` or `script -q -c`. In both cases, a `<prompt>` placeholder is directly concatenated into the shell command string. If this prompt originates from untrusted user input and is not properly sanitized by the calling agent, it can lead to arbitrary command execution on the host system.
- Evidence:
    - `Command template: - ~/.npm-global/bin/gemini -p "<prompt>"`
    - `If pty:true still behaves poorly, use a pseudo-tty wrapper: - script -q -c "~/.npm-global/bin/gemini -p \"<prompt>\"" /dev/null`
- Why it may be benign or suspicious: Benign in its intent to execute the `gemini` CLI for its stated purpose. Suspicious and high-risk due to the direct, unsanitized embedding of a variable (`<prompt>`) into a shell command, which is a classic command injection vulnerability. The skill itself does not implement any sanitization, offloading this critical security responsibility entirely to the potentially unaware calling agent.

### Behavior: External Network Communication
- Category: Legitimate Functionality
- Technique ID (if applicable): E1 — ExternalTransmission (for search queries)
- Severity: LOW
- Description: The core purpose of the skill is to perform web searches using the Gemini CLI, which inherently requires making external network requests to retrieve search results.
- Evidence: "Use Gemini CLI ... to do web search / fact-finding", "Search the web: <topic>"
- Why it may be benign or suspicious: This is a benign and expected behavior for a web search tool. It is not suspicious unless there is evidence of exfiltrating data unrelated to the search query.

### Behavior: Filesystem Access (Executable)
- Category: Legitimate Functionality
- Technique ID (if applicable): None (specific file access, not enumeration)
- Severity: LOW
- Description: The skill specifies the path to the `gemini` CLI executable, `~/.npm-global/bin/gemini`, for execution.
- Evidence: `~/.npm-global/bin/gemini`
- Why it may be benign or suspicious: Benign, as it's standard practice for executing a locally installed command-line interface tool.

### Behavior: Skill Installation via `curl`
- Category: Legitimate Functionality
- Technique ID (if applicable): SC2 — RemoteScriptExecution (potential vector, but not direct execution of the downloaded content)
- Severity: LOW
- Description: The `metadata.json` specifies an `install_command` that uses `curl` to download the `SKILL.md` file from a GitHub raw URL. This is a common method for installing agent skills.
- Evidence: `install_command": "mkdir -p .claude/skills/router && curl -sL \"https://raw.githubusercontent.com/majiayu000/claude-skill-registry/main/skills/development/router/SKILL.md\" > .claude/skills/router/SKILL.md"`
- Why it may be benign or suspicious: Benign for installation. The downloaded `SKILL.md` is a markdown file containing instructions, not an executable script itself. However, if the source URL were compromised, it could lead to the installation of malicious instructions.

## Suspicious Indicators
- **Dangerous commands/APIs**: The explicit instruction to use `functions.exec` or `script -q -c` with direct string concatenation of user-controlled input (`<prompt>`) is a dangerous pattern that directly enables command injection.
- **Metadata Inconsistency**: The `metadata.json` identifies the skill as "router" with a description of an "Intelligent routing layer," while the `_meta.json` and `SKILL.md` clearly define it as "gemini-web-search." The `install_command` also places the `gemini-web-search` `SKILL.md` into a `router` directory. This inconsistency suggests potential misconfiguration, mislabeling, or a repurposed skill, which can sometimes be a red flag for obfuscation or confusion, though in this case, it seems more like an administrative error.

## Hidden or Undocumented Functionality
None detected. The skill's description and the instructions within `SKILL.md` are consistent and clearly explain its purpose and operational methods.

## Final Assessment
The skill is classified as **MALICIOUS** not due to overt malicious intent in its stated purpose, but because its implementation presents a critical security vulnerability: **command injection (SC1)**. By directly embedding a user-controlled `<prompt>` into a shell command without any internal sanitization, the skill creates a high-risk avenue for arbitrary command execution. An attacker or a poorly designed agent could easily exploit this to run any command on the system where the agent operates. This design flaw constitutes a high-risk behavior that can be readily leveraged for harmful purposes, making the skill inherently dangerous.

## Recommended Action
BLOCK
The severe command injection vulnerability poses an unacceptable risk. The skill should be blocked until the command execution mechanism is redesigned to prevent arbitrary command injection, either by implementing robust sanitization within the skill or by using a safer execution API that does not allow direct shell command construction from untrusted input.