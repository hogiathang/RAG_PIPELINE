# Agent Skill Security Analysis Report

## Overview
- Skill Name: advanced-tool-usage
- Declared Purpose: Guidelines for multi-stage tool orchestration and handling large data using 'redirect_tool_call'. Use this when you need to process large amounts of data without exhausting the context window or when building complex data pipelines.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: This skill is a documentation-only skill providing guidelines and patterns for an agent to effectively use various tools, particularly `redirect_tool_call`, `python_execute`, and `shell_execute`, for processing large datasets and orchestrating multi-stage operations. It does not contain executable code itself but rather instructs the agent on best practices. While it references powerful tools that could be misused, the skill itself promotes legitimate and efficient data handling techniques.

## Observed Behaviors

### Behavior
- Category: Agent Manipulation (Instructional)
- Technique ID (if applicable): P1 — InstructionOverride (indirectly, as it guides agent behavior)
- Severity: LOW
- Description: The skill provides explicit instructions and patterns for the agent on how to use various tools (`redirect_tool_call`, `python_execute`, `shell_execute`, `cat`, `tavily_search`, `rg`, `grep`, `mktemp -d`). This guides the agent's decision-making process for tool selection and orchestration.
- Evidence: The entire `SKILL.md` content, which is a set of guidelines and patterns.
- Why it may be benign or suspicious: This is benign. The purpose of such a skill is to improve agent performance and adherence to best practices. It's a form of "meta-instruction" for the agent.

### Behavior
- Category: File System Access
- Technique ID (if applicable): E3 — FileSystemEnumeration (indirectly, through described patterns)
- Severity: LOW
- Description: The skill describes patterns involving reading from and writing to temporary files and directories (e.g., `redirect_tool_call` with `output_file`, `mktemp -d`, using `cat`, `rg`, `grep` on files).
- Evidence: "Call the second tool (e.g., `python_execute` or `shell_execute`) and pass the file path created in step 1 as an argument.", "Redirect the reading tool (e.g., `cat`, `tavily_search`) to a temporary file.", "Use `shell_execute` with `mktemp -d` to create a dedicated scratch directory.", "Example: `redirect_tool_call(..., output_file="/tmp/tmp.X/step1.json")`"
- Why it may be benign or suspicious: This is benign. These are standard and necessary operations for processing large data, creating pipelines, and managing workspace, which is the declared purpose of the skill.

### Behavior
- Category: Remote Execution (Instructional)
- Technique ID (if applicable): SC2 — RemoteScriptExecution (indirectly, through described patterns)
- Severity: LOW
- Description: The skill instructs the agent on how to use `python_execute` and `shell_execute` for processing data, which are tools capable of executing arbitrary code.
- Evidence: "Call the second tool (e.g., `python_execute` or `shell_execute`) and pass the file path created in step 1 as an argument."
- Why it may be benign or suspicious: This is benign in the context of *this skill*. The skill itself does not execute code; it provides guidance on using existing, powerful tools. The inherent risk of `python_execute` and `shell_execute` is high, but this skill merely documents their legitimate use for data processing within a pipeline. It does not provide malicious commands or encourage misuse.

### Behavior
- Category: External Interaction (Instructional)
- Severity: LOW
- Description: The skill mentions `tavily_search` as a tool that can be redirected to a temporary file, implying external network requests for information retrieval.
- Evidence: "Redirect the reading tool (e.g., `cat`, `tavily_search`) to a temporary file."
- Why it may be benign or suspicious: This is benign. `tavily_search` is a legitimate search tool, and its use for gathering information is a common agent task. The instruction to redirect its output is for context economy, not for malicious exfiltration.

## Suspicious Indicators
- Sensitive data access: None directly. The skill discusses processing "large amounts of data," which *could* be sensitive, but it does not specify *what* data or provide mechanisms for unauthorized access or exfiltration.
- Network endpoints: Mentions `tavily_search`, which implies legitimate external network requests for search queries. No suspicious endpoints are indicated.
- Dangerous commands/APIs: The skill references `shell_execute` and `python_execute`, which are inherently powerful and dangerous if misused. However, this skill only provides benign, instructional patterns for their use in data processing pipelines, not malicious commands.

## Hidden or Undocumented Functionality
None detected. The skill is a markdown document explicitly outlining its purpose and patterns.

## Final Assessment
The skill is classified as **BENIGN**. It is a documentation skill designed to guide an agent in the efficient and structured use of its available tools for complex data processing tasks. It promotes best practices like context economy and pipelining. While it references powerful tools (`shell_execute`, `python_execute`) that carry inherent risks if misused, the skill itself does not contain any executable code, nor does it instruct the agent to perform any malicious actions such as credential theft, data exfiltration, or privilege abuse. Its content is entirely consistent with its declared purpose.

## Recommended Action
ALLOW
The skill provides valuable guidance for agents to operate more effectively and efficiently, especially when dealing with large datasets. There is no evidence of malicious intent or high-risk behavior within the skill itself.