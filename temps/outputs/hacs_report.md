# Agent Skill Security Analysis Report

## Overview
- Skill Name: web-research
- Declared Purpose: Perform web research using OpenAI APIs at various depth levels, saving results locally.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The skill's declared purpose and described functionality are benign, focusing on web research via OpenAI APIs and local storage of results. However, the core executable script (`research.py`) is not provided for static analysis, and its installation is not explicitly covered by the `install_command`. This introduces an unverified component, elevating the overall risk despite the benign description.

## Observed Behaviors

### Behavior: Skill Installation (Documentation Download)
- Category: File System Write / Remote Content Fetch
- Technique ID (if applicable): None directly applicable (not executing downloaded content)
- Severity: LOW
- Description: The `install_command` downloads the `SKILL.md` file (which is the skill's documentation) from a GitHub raw content URL into the designated skill directory.
- Evidence: `metadata.json` -> `install_command`: `curl -sL "https://raw.githubusercontent.com/dimitri-vs/elevate-agent-skills/main/web-research/SKILL.md" > .claude/skills/web-research/SKILL.md`
- Why it may be benign or suspicious: This behavior is benign as it only downloads a non-executable markdown file. While `curl` from raw GitHub can be a vector for supply chain attacks, in this specific instance, the downloaded content is documentation.

### Behavior: Local Script Execution
- Category: Remote Execution (from the agent's perspective, it's executing a skill's script)
- Technique ID (if applicable): SC2 — RemoteScriptExecution
- Severity: MEDIUM
- Description: The skill's `SKILL.md` documentation instructs the agent to execute a local Python script named `research.py` using the `uv run` command. This script is described as performing web research.
- Evidence: `SKILL.md` -> `Usage` section: `cd "<skill-directory>" && uv run research.py ...`. Also, `metadata.json` -> `has_scripts: true`.
- Why it may be benign or suspicious: This behavior is benign if the `research.py` script adheres to its description. However, the actual source code for `research.py` is not provided for static analysis, and its installation is not explicitly part of the `install_command`. The execution of an unverified script represents a significant risk, as arbitrary code execution could lead to malicious activities.

### Behavior: Credential Access (OPENAI_API_KEY)
- Category: Credential Handling
- Technique ID (if applicable): PE3 — CredentialFileAccess
- Severity: LOW
- Description: The `research.py` script is described as accessing the `OPENAI_API_KEY` from local `.env` files (current directory, user home, skill directory) or system environment variables for authentication with OpenAI APIs.
- Evidence: `SKILL.md` -> `Credentials` section.
- Why it may be benign or suspicious: This is a standard and necessary practice for any skill interacting with an API requiring authentication. There is no evidence in the provided text of the key being exfiltrated or misused, only accessed for its stated purpose.

### Behavior: External API Communication (OpenAI)
- Category: Data Exfiltration (of user query)
- Technique ID (if applicable): E1 — ExternalTransmission
- Severity: LOW
- Description: The skill sends user research queries to OpenAI's API endpoints (`gpt-5-search-api`, `o3-deep-research`) for processing.
- Evidence: `metadata.json` description, `SKILL.md` description and `Configuration` table.
- Why it may be benign or suspicious: This is the core functionality of a web research skill. The data transmitted is the user's explicit research query, which is expected for the skill's operation. No evidence of other sensitive data being exfiltrated.

### Behavior: Local File System Write (Research Results)
- Category: File System Access
- Technique ID (if applicable): None directly applicable
- Severity: LOW
- Description: The skill saves the markdown-formatted research results to a dedicated `~/research/` directory in the user's home folder.
- Evidence: `SKILL.md` -> `Output` and `Saved Research` sections.
- Why it may be benign or suspicious: This is a benign behavior, as it serves to store the output of the skill for the user's benefit.

## Suspicious Indicators
- Sensitive data access: The skill accesses `OPENAI_API_KEY`. While necessary for its function, the lack of `research.py`'s source code means its handling of this key cannot be fully verified.
- Network endpoints: Communication with `raw.githubusercontent.com` (for install) and OpenAI API endpoints (for research). Both are legitimate for the stated purpose.
- Dangerous commands/APIs: The skill instructs the agent to execute `uv run research.py`. The `research.py` script itself is not provided for analysis, making its actual behavior unknown.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` provides a comprehensive description of the skill's purpose, usage, configuration, and output. The primary unknown is the actual code of `research.py`, but its *described* functionality is well-documented.

## Final Assessment
Based on the provided `metadata.json` and `SKILL.md`, the skill is classified as **BENIGN**. All described behaviors align with its stated purpose of performing web research using OpenAI APIs. There is no direct evidence of malicious intent, credential theft, unauthorized data exfiltration, privilege abuse, or agent manipulation within the provided text.

However, the overall risk level is assessed as **MEDIUM** due to the critical dependency on an external Python script (`research.py`) whose source code is not provided for analysis. The `install_command` only installs the `SKILL.md` file, not `research.py`, creating a gap in the verifiable installation process of the executable component. While the *description* of `research.py`'s behavior is benign, the inability to statically analyze the actual script means its true actions remain unverified.

## Recommended Action
REVIEW
The skill's described functionality is benign, but the core executable (`research.py`) is not provided for analysis, and its installation is not explicitly detailed in the `install_command`. This introduces an unverified component that could potentially harbor malicious code. A manual review of the `research.py` script's source code is necessary to confirm its benign nature before allowing full execution.