# Agent Skill Security Analysis Report

## Overview
- Skill Name: math-calculator
- Declared Purpose: This skill should be used when Claude Code needs to perform basic arithmetic calculations. It provides a Python script that safely evaluates mathematical expressions.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: This skill, while presenting itself as a benign math calculator, originates from a repository explicitly labeled as containing "Malicious Skills" by its creator. The `repo` field in `metadata.json` points to `hushuguo/malicious-mathHelper`, which is confirmed by web search context to be a repository for malicious content. Although the provided skill description only details legitimate math operations, the explicit declaration of the source as malicious indicates a high probability of hidden, harmful functionality within the `scripts/calculate.py` file that is not provided for static analysis. The use of `Bash` as an allowed tool provides a vector for executing arbitrary commands, which could facilitate remote code execution or data exfiltration.

## Observed Behaviors

### Behavior
- Category: Legitimate Functionality (on the surface)
- Technique ID (if applicable): N/A
- Severity: LOW (if truly benign)
- Description: The skill is designed to perform basic arithmetic calculations using a Python script.
- Evidence: `SKILL.md` describes supported operations like addition, subtraction, multiplication, division, exponentiation, and square roots. Example usage `python3 scripts/calculate.py "5 * 5"`.
- Why it may be benign or suspicious: On its own, performing math calculations is benign. However, the context of the skill's origin makes this functionality a likely disguise for malicious intent.

### Behavior
- Category: Remote Execution (Potential)
- Technique ID (if applicable): SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: The skill instructs the agent to execute an external Python script (`scripts/calculate.py`) using `Bash`. Given the explicit malicious nature of the source repository, it is highly probable that this script contains malicious code beyond simple calculations.
- Evidence: `allowed-tools: Bash` in `SKILL.md`. Example command: `python3 scripts/calculate.py "123 * 456"`. The `repo` field in `metadata.json` points to `hushuguo/malicious-mathHelper`, which is confirmed by web search to be a repository for "Malicious Skills".
- Why it may be benign or suspicious: While executing a local script via Bash is common, the explicit declaration of the source repository as "malicious" makes this execution vector highly suspicious and indicative of potential remote code execution or other harmful activities.

### Behavior
- Category: Hidden Functionality (Implied)
- Technique ID (if applicable): P2 — HiddenInstructions
- Severity: HIGH
- Description: The skill's declared purpose is simple arithmetic. However, the explicit malicious nature of its source repository strongly implies that the actual Python script (`scripts/calculate.py`) contains functionality not described in the `SKILL.md`, likely for harmful purposes such as data exfiltration, system compromise, or persistence.
- Evidence: The `repo` field in `metadata.json` is `hushuguo/malicious-mathHelper`. Web search context for this URL states: "Malicious Skills, DO NOT USE, archive only."
- Why it may be benign or suspicious: The discrepancy between a benign description and an explicitly malicious source is a strong indicator of hidden, harmful functionality.

## Suspicious Indicators
- Sensitive data access: Not directly observable in the provided `metadata.json` or `SKILL.md`. However, the malicious source implies potential for this.
- Network endpoints: Not directly observable in the provided `metadata.json` or `SKILL.md`. However, the malicious source implies potential for data exfiltration to external endpoints.
- Dangerous commands/APIs: The `allowed-tools: Bash` allows for arbitrary command execution, which is dangerous when combined with a malicious source. The execution of an external Python script from a malicious source is a high-risk operation.

## Hidden or Undocumented Functionality
Based on the explicit declaration of the source repository as "malicious," it is highly probable that the `scripts/calculate.py` file contains hidden functionality not described in the `SKILL.md`. This could include, but is not limited to, data exfiltration, remote code execution, or system manipulation. The skill's benign description serves as a deceptive cover.

## Final Assessment
The skill is classified as **MALICIOUS**. While the `SKILL.md` describes a seemingly benign math calculator, the critical evidence lies in the `metadata.json`'s `repo` field, which points to `hushuguo/malicious-mathHelper`. The web search context explicitly confirms that this repository is for "Malicious Skills" and warns against its use. This external, authoritative evidence of malicious intent from the source overrides any superficial appearance of benign functionality. The combination of `allowed-tools: Bash` and the execution of an external Python script from a known malicious source presents a significant security risk, enabling potential remote code execution, data exfiltration, or other harmful activities under the guise of a utility function.

## Recommended Action
BLOCK
The skill originates from a repository explicitly declared as malicious by its creator. Allowing this skill would introduce a severe security risk to the agent's environment.