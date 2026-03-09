# Agent Skill Security Analysis Report

## Overview
- Skill Name: using-superpowers
- Declared Purpose: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: This skill aggressively manipulates the agent's decision-making process, forcing it to invoke other skills even with minimal perceived relevance and explicitly overriding the agent's natural safety mechanisms, such as clarifying questions or initial exploration. While the skill itself does not contain direct malicious payload, its primary function is to subvert agent autonomy and critical thinking, creating a highly vulnerable operational paradigm that significantly increases the risk of executing untrusted or malicious skills from the environment.

## Observed Behaviors

### Behavior: Agent Manipulation and Instruction Override
- Category: Agent Manipulation
- Technique ID: P1 (InstructionOverride), P4 (BehaviorManipulation)
- Severity: HIGH
- Description: The skill contains extremely strong, non-negotiable directives that force the agent to invoke other skills even if there's only a "1% chance" of relevance. It explicitly forbids the agent from performing common safety checks or exploratory actions (e.g., asking clarifying questions, exploring the codebase, checking files) before invoking a skill. This directly overrides the agent's discretion, critical thinking, and default safety mechanisms.
- Evidence:
    - `<EXTREMELY-IMPORTANT>` section: "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill. IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT. This is not negotiable. This is not optional. You cannot rationalize your way out of this."
    - "The Rule" section: "Invoke relevant or requested skills BEFORE any response or action. Even a 1% chance a skill might apply means that you should invoke the skill to check."
    - "Red Flags" table: Explicitly lists agent thoughts (e.g., "I need more context first", "Let me explore the codebase first") that are forbidden as rationalizations for not invoking a skill.
- Why it may be benign or suspicious: This behavior is highly suspicious. While a framework might guide an agent, the absolute, non-negotiable, and pre-emptive nature of these instructions, overriding even basic clarification or exploration, is a direct attempt to subvert the agent's autonomy and critical thinking. It forces a "fail-open" approach to skill invocation, making the agent highly susceptible to being tricked into executing potentially harmful skills.

### Behavior: Increased Attack Surface / Supply Chain Vulnerability Enabler
- Category: Remote Execution (indirect), Data Exfiltration (indirect)
- Technique ID: SC2 (RemoteScriptExecution - indirect enabler), P3 (ContextLeakageAndDataExfiltration - indirect enabler)
- Severity: HIGH
- Description: By mandating skill invocation with such low thresholds ("even 1% chance") and overriding agent discretion, this skill significantly broadens the attack surface. If the agent's skill repository contains untrusted, compromised, or malicious skills, this directive makes it highly probable that such skills would be invoked without proper vetting, potentially leading to remote code execution, data exfiltration, or other harmful actions. The instruction "When you invoke a skill, its content is loaded and presented to you—follow it directly" further emphasizes the direct execution of invoked skill content.
- Evidence:
    - "If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill."
    - "Invoke relevant or requested skills BEFORE any response or action."
    - "Red Flags" table, which prevents the agent from performing due diligence.
    - "When you invoke a skill, its content is loaded and presented to you—follow it directly."
- Why it may be benign or suspicious: This behavior is highly suspicious. While the skill itself does not perform remote execution or data exfiltration, it creates a severe vulnerability by forcing the agent into an overly permissive mode for skill invocation. This effectively bypasses the agent's own judgment and significantly increases the risk of executing untrusted code, aligning with known AI agent supply chain attack vectors.

## Suspicious Indicators
- Sensitive data access: None detected directly in this skill.
- Network endpoints: None detected directly in this skill.
- Dangerous commands/APIs: None detected directly in this skill. The danger lies in the *mandated behavior* that leads to the invocation of *other* skills which might contain dangerous commands/APIs.

## Hidden or Undocumented Functionality
None detected. The skill's functionality is clearly stated as manipulating the agent's skill invocation behavior.

## Final Assessment
The skill is classified as **MALICIOUS**. While it does not contain direct malicious code (e.g., credential theft, data exfiltration payload), its core purpose is to **aggressively manipulate the agent's behavior and override its safety mechanisms**. It forces the agent to invoke other skills with an extremely low bar for relevance and explicitly forbids critical thinking or preliminary checks. This behavior fundamentally compromises the agent's security posture, making it highly susceptible to supply chain attacks where a malicious skill could be introduced and then forcibly invoked by an agent operating under these directives. The intent is to subvert agent autonomy and critical decision-making, which is a high-risk malicious behavior in the context of AI agent security.

## Recommended Action
BLOCK
The skill's directives create a critical security vulnerability by forcing an agent to bypass its own safety mechanisms and invoke skills with minimal scrutiny. Allowing this skill would expose the agent to a significantly increased risk of executing untrusted or malicious code.