# Agent Skill Security Analysis Report

## Overview
- Skill Name: skill-discovery-patterns
- Declared Purpose: How the Rails Enterprise Dev plugin discovers and uses project skills dynamically
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: This skill describes a core mechanism for an AI agent to discover and dynamically invoke other "skills" from a local, user-controlled directory. While the skill itself is documentation, the described process, when combined with the understanding that Agent Skills can contain executable code (as per external context), introduces a significant attack surface for arbitrary code execution and agent manipulation. It outlines a pattern that enables local arbitrary code execution via malicious skill injection.

## Observed Behaviors

### Behavior: File System Enumeration
- Category: Legitimate Functionality (but part of a risky chain)
- Technique ID (if applicable): E3 — FileSystemEnumeration
- Severity: LOW (in isolation)
- Description: The skill describes the plugin scanning the `.claude/skills/` directory to find available skills.
- Evidence: "At workflow start, the plugin scans `.claude/skills/` to find available skills"
- Why it may be benign or suspicious: Scanning a local directory is a normal operation for a discovery mechanism. However, when combined with dynamic invocation of content from that directory, it becomes a critical step in a potential attack chain.

### Behavior: Local Script Execution (Plugin-provided)
- Category: Legitimate Functionality (but part of a risky chain)
- Technique ID (if applicable): SC2 — RemoteScriptExecution (local variant)
- Severity: LOW (in isolation)
- Description: The skill explicitly states that the plugin executes a bash script (`discover-skills.sh`) located within the plugin's root directory to perform skill discovery.
- Evidence: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/scripts/discover-skills.sh`
- Why it may be benign or suspicious: The script is described as being part of the trusted plugin root. However, if this script itself has vulnerabilities (e.g., command injection when processing skill names from the user-controlled directory), or if the `CLAUDE_PLUGIN_ROOT` can be manipulated, it could be exploited. Based on the provided text, the script's origin is trusted.

### Behavior: Dynamic Skill Invocation from User-Controlled Directory
- Category: Remote Execution / Agent Manipulation (enabling mechanism)
- Technique ID (if applicable): SC2 — RemoteScriptExecution, P4 — BehaviorManipulation
- Severity: HIGH
- Description: The skill describes a system where agents dynamically "invoke" and "use" skills discovered from a local, user-controlled directory (`.claude/skills/`). External context indicates that "Agent Skills can include Python scripts... Malicious Skills can exploit this to execute arbitrary code in Agent environment." This implies that the system described by this skill enables the execution of potentially untrusted code or instructions from a local source, leading to arbitrary code execution or manipulation of the agent's behavior.
- Evidence:
    - "The Rails Enterprise Dev plugin... automatically discovers and uses skills from your project's `.claude/skills/` directory"
    - "Dynamic Skill Invocation: Throughout the workflow, agents check for and use available skills"
    - "Invoke skill: 'I need guidance from activerecord-patterns skill for implementing User model'"
    - "Custom Skill Integration: Add project-specific skills... Plugin auto-discovers on next run... Uses my-custom-skill during implementation"
    - Web search context: "Agent Skills can include Python scripts with PEP 723 inline metadata. However, the attacker retains the ability to publish a malicious version of `halo4`, leading to deferred code execution on all new skill executions." and "Malicious Skills can exploit this to execute arbitrary code in Agent environment or worse, align the agent to perform malicious actions."
- Why it may be benign or suspicious: While the intent is to provide flexibility and extensibility, allowing dynamic invocation of content (potentially executable code) from a user-controlled local directory without explicit mention of sandboxing or strict validation creates a significant attack vector. A malicious actor could place a harmful skill in `.claude/skills/`, which would then be discovered and "invoked" by the agent, leading to arbitrary code execution or manipulation of the agent's behavior.

## Suspicious Indicators
- Sensitive data access: None directly observed in this skill.
- Network endpoints: None directly observed in this skill.
- Dangerous commands/APIs: The skill describes a mechanism that enables the execution of potentially dangerous commands/APIs if the discovered skills contain them. The `bash` command for `discover-skills.sh` is mentioned, but its source is the plugin root.

## Hidden or Undocumented Functionality
None detected. The skill is documentation and is quite explicit about the functionality it describes.

## Final Assessment
The skill is classified as **MALICIOUS** not because its own markdown content performs malicious actions, but because it describes and enables a highly dangerous mechanism within the Agent Skill ecosystem. It outlines a process for dynamic discovery and invocation of "skills" from a user-controlled local directory (`.claude/skills/`). Given the external context that Agent Skills can contain executable code and can be exploited for arbitrary code execution, this skill effectively defines a local arbitrary code execution vulnerability. An attacker could place a malicious skill in the `.claude/skills/` directory, which would then be discovered and "invoked" by the agent, leading to the execution of harmful code or manipulation of the agent's actions. This represents a significant supply chain risk or local privilege escalation vector.

## Recommended Action
BLOCK
The described skill discovery and invocation pattern, without explicit mention of robust security controls (like sandboxing or strict content validation for discovered skills), poses a severe risk of arbitrary code execution. Allowing this pattern would open the door to local supply chain attacks where malicious skills could be injected into a project's `.claude/skills/` directory. This fundamental mechanism needs a thorough security review and robust hardening before being allowed.