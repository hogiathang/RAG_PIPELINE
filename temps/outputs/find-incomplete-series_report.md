# Agent Skill Security Analysis Report

## Overview
- Skill Name: find-incomplete-series
- Declared Purpose: Find incomplete series in your Calibre library and identify the next book to read in each series.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The skill is designed to interact with a local Calibre library to identify incomplete book series. It achieves this by executing a local Python script. While the execution of local scripts presents a general attack surface, the declared purpose and described actions are entirely legitimate and do not show any indicators of malicious intent based on the provided metadata and skill description.

## Observed Behaviors

### Behavior: Local Script Execution
- Category: Remote Execution (as a general capability, though local in this context)
- Technique ID (if applicable): SC2 — RemoteScriptExecution (The agent is instructed to execute a script, which is a form of remote execution from the agent's perspective, even if the script is local to the skill package.)
- Severity: LOW (in this specific case, as the script's described purpose is benign)
- Description: The skill instructs the agent to execute a Python script (`series.py`) located within its own directory (`__SKILL_DIR__/scripts/series.py`).
- Evidence: `python3 __SKILL_DIR__/scripts/series.py` in `SKILL.md`.
- Why it may be benign or suspicious: This is a common and necessary mechanism for agent skills to perform complex tasks. It is benign if the script performs only the described, legitimate actions. It would be suspicious if the script's content (which is not provided for analysis) contained malicious code, but there is no evidence of that here. The skill explicitly states what the script will do, and it aligns with the declared purpose.

### Behavior: Local Data Access (Calibre Library)
- Category: FileSystemEnumeration / Data Access
- Technique ID (if applicable): E3 — FileSystemEnumeration (for querying the library)
- Severity: LOW
- Description: The script is designed to query the user's local Calibre library for book and series information.
- Evidence: "Query your Calibre library for all books that are part of a series", "Identify series where you've read at least one book but haven't finished the entire series" in `SKILL.md`.
- Why it may be benign or suspicious: Accessing local data is benign when it is directly related to the skill's declared purpose and is performed in a read-only or non-destructive manner. The description implies read-only access for analysis. It would be suspicious if the skill attempted to modify, delete, or exfiltrate this data without explicit user consent or clear justification, which is not indicated here.

## Suspicious Indicators
- Sensitive data access: None indicated beyond the Calibre library data, which is the skill's explicit target.
- Network endpoints: None indicated. The skill description focuses on local library interaction.
- Dangerous commands/APIs: The execution of a local Python script (`python3`) is a powerful capability. However, it is the primary mechanism for many legitimate skills. Without the script's content, we cannot determine if the specific commands within `series.py` are dangerous. The skill explicitly warns against invoking `calibredb` commands directly, implying the script handles this interaction safely.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` clearly describes the script's purpose and steps, which align with the `metadata.json` description. The "Important!" notes are instructions to the agent regarding skill execution, not hidden functionality.

## Final Assessment
The skill is classified as **BENIGN**.
The analysis is based solely on the provided `metadata.json` and `SKILL.md`. The declared purpose is clear and legitimate: to help users manage their Calibre book series. The method involves executing a local Python script, which is a common and often necessary pattern for agent skills to perform complex, local operations. While the capability to execute arbitrary Python code carries inherent risk, there is no evidence in the provided materials to suggest malicious intent or high-risk behavior beyond the legitimate scope of the skill. The description of the script's actions aligns perfectly with the stated purpose, focusing on querying and identifying information within a local Calibre library.

## Recommended Action
ALLOW
The skill's description and metadata indicate a benign purpose and functionality. The execution of a local Python script is a standard mechanism for agent skills. Without evidence of malicious code within the `series.py` script itself (which is not provided for analysis), there is no basis to block this skill.