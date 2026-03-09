# Agent Skill Security Analysis Report

## Overview
- Skill Name: linkedin
- Declared Purpose: Create LinkedIn posts for lead generation and thought leadership, including specific voice, format, and rhythm guidance.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The skill definition is purely declarative, providing instructions and references to local markdown files for context and templates. It does not contain any executable code, network requests, or direct manipulation instructions. Its purpose is clearly defined and benign, focusing on content generation.

## Observed Behaviors

### Behavior: Content Generation Guidance
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill provides detailed instructions and guidelines for creating LinkedIn posts, including target length, hook requirements, and a weekly posting rhythm.
- Evidence: "Target length: 1,200-1,800 characters", "Hook: Under 140 characters", "Weekly rhythm: Tuesday: Framework or template, Wednesday: Industry take or observation, Thursday: Personal lesson or behind-the-scenes"
- Why it may be benign or suspicious: This is the core, declared functionality of the skill and is entirely benign.

### Behavior: Local File Referencing
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill references several local markdown files (`context/voice.md`, `context/format.md`, `context/rhythm.md`, `docs/guides/brand-guide.md`, `templates/post.md`) to provide additional context, guidelines, and templates.
- Evidence: "Context Files: `context/voice.md` - LinkedIn-specific voice...", "Brand Reference: See `docs/guides/brand-guide.md`...", "Templates: `templates/post.md` - LinkedIn post template"
- Why it may be benign or suspicious: Referencing local files for context and templates is a common and legitimate practice for agent skills to access supplementary information. The `SKILL.md` itself does not instruct the agent to *execute* these files, but rather to *read and interpret* them as guidance. There is no indication of remote file fetching or execution.

## Suspicious Indicators
- Sensitive data access: None detected.
- Network endpoints: None detected.
- Dangerous commands/APIs: None detected. The skill definition is purely descriptive and does not contain any executable commands or API calls.

## Hidden or Undocumented Functionality
None detected. The skill's capabilities are clearly explained in its description and quick reference sections.

## Final Assessment
The skill is classified as **BENIGN**. The provided `SKILL.md` file is a declarative definition of an agent's capability to generate LinkedIn content. It outlines instructions, guidelines, and references to local, non-executable markdown files for additional context. There is no evidence of executable code, network activity, credential harvesting, data exfiltration, privilege abuse, or any other malicious behavior within the scope of this static analysis. The web search context highlights the *potential* for Agent Skills to be malicious if they contain scripts or hidden instructions, but this specific skill does not exhibit such characteristics.

## Recommended Action
ALLOW
The skill appears safe for use as it aligns with its declared purpose and shows no malicious indicators.