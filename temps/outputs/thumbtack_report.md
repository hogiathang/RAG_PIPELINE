# Agent Skill Security Analysis Report

## Overview
- Skill Name: Local Falcon - AI Visibility & Local SEO Expert
- Declared Purpose: To equip AI agents with expert-level knowledge and guidance on AI Visibility Optimization and Local SEO, including Google Business Profile management, geo-grid rank tracking, and optimization for various AI platforms (ChatGPT, Gemini, AI Mode, AI Overviews, Grok). It also details integration with a companion `@local-falcon/mcp` server for live data analysis and scan execution.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The skill is primarily a comprehensive knowledge base and set of instructions for an AI agent, designed to provide expert guidance on local SEO and AI visibility. It describes how an agent can interact with a separate, explicitly mentioned MCP (Managed Capability Provider) server (`@local-falcon/mcp`) to access live data and execute scans on the Local Falcon platform. All described behaviors are consistent with its declared purpose, and there is no evidence of malicious intent or high-risk activities within the skill's code or metadata.

## Observed Behaviors

### Behavior: Knowledge Provisioning and Expert Guidance
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill provides extensive, structured information and best practices related to local SEO, AI visibility, and the Local Falcon platform's metrics and tools. It includes deep dives into various AI platforms' local search behaviors and optimization strategies.
- Evidence: `AGENTS.md`, `SKILL.md`, `README.md`, `marketplace.json` all contain detailed descriptions, definitions, strategies, and guidelines for the AI agent.
- Why it may be benign or suspicious: This is the core, benign purpose of the skill, acting as an expert knowledge base for the agent.

### Behavior: Integration with External Managed Capability Provider (MCP)
- Category: External Interaction / Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill is designed to integrate with a separate `@local-falcon/mcp` server. It describes how the agent can detect the availability of MCP tools (e.g., `listLocalFalconScanReports`, `runLocalFalconScan`) and switch between "Orchestration Mode" (with live data) and "Guidance Mode" (without live data). The skill provides instructions for users to install and configure this MCP server, including setting an API key.
- Evidence:
    - `AGENTS.md`: "MCP Server - package: @local-falcon/mcp - capabilities: live_data_retrieval, scan_execution, account_management"
    - `SKILL.md`: "MCP Integration: "@local-falcon/mcp"", "If tools like `listLocalFalconScanReports`, `viewLocalFalconAccountInformation`, `runLocalFalconScan` are available..."
    - `README.md`: "Pair this skill with the [@local-falcon/mcp](https://www.npmjs.com/package/@local-falcon/mcp) server..."
    - `marketplace.json`: `related.mcp_server` section.
    - `SKILL.md` provides explicit instructions for configuring `LOCAL_FALCON_API_KEY` in the Claude Code MCP settings (`~/.config/claude/mcp.json`).
- Why it may be benign or suspicious: This is a legitimate pattern for AI agents to extend their capabilities by interacting with external services through a dedicated server. The skill itself does not handle the API key directly but instructs the user on how to configure it for the *companion MCP server*. The MCP server, not the skill, would then perform the actual API calls to `localfalcon.com`. This separation of concerns is a good practice.

### Behavior: File System Interaction (Installation Instructions)
- Category: Legitimate Functionality (Installation)
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill provides instructions for its installation, which involves copying files to a specific directory (`~/.config/claude/skills/`) and configuring a JSON file (`~/.config/claude/mcp.json`).
- Evidence:
    - `README.md`: `cp -r node_modules/@local-falcon/local-visibility-skill ~/.config/claude/skills/local-falcon`
    - `SKILL.md`: "Add to your Claude Code MCP settings (usually `~/.config/claude/mcp.json` or similar)"
    - `marketplace.json`: `install.instructions`
- Why it may be benign or suspicious: These are standard installation steps for an agent skill and its companion server. They describe how the user *installs* the skill, not a runtime behavior of the skill itself.

## Suspicious Indicators (if any)
- Sensitive data access: The skill *mentions* the need for a `LOCAL_FALCON_API_KEY` for the companion MCP server, but the skill itself does not access or handle this key. It instructs the user on how to configure it for the *MCP server*. This is a standard and expected pattern for integrating with a commercial API.
- Network endpoints: The skill itself, being a collection of markdown and JSON files, does not directly initiate network connections. The companion `@local-falcon/mcp` server, once installed and configured, would communicate with `localfalcon.com` as its declared purpose.
- Dangerous commands/APIs: The skill describes the use of tools like `runLocalFalconScan` which would trigger actions on the Local Falcon platform via the MCP server. These are specific to the Local Falcon service and are part of its legitimate functionality. There are no generic or arbitrary command execution instructions.

## Hidden or Undocumented Functionality
None detected. All capabilities, including the integration with the MCP server and the types of data/actions involved, are clearly described across the various documentation files.

## Final Assessment
The skill is classified as **BENIGN**. The analysis of the provided files (`AGENTS.md`, `_meta.json`, `metadata.json`, `package.json`, `README.md`, `SKILL.md`, `marketplace.json`) reveals that the skill functions as a comprehensive knowledge base and an instructional guide for an AI agent. Its primary purpose is to enable the agent to provide expert advice on local SEO and AI visibility, leveraging data from the Local Falcon platform via a separate, explicitly mentioned MCP server.

There is no executable code within the skill itself that could perform malicious actions. The interaction with external services (Local Falcon API) is clearly documented as being handled by a companion MCP server, which the user must explicitly install and configure with an API key. This separation of concerns and transparent declaration of functionality indicates a legitimate and well-intentioned design. The web search context also confirms Local Falcon as a legitimate company providing local SEO services.

## Recommended Action
ALLOW
The skill is benign and serves its declared purpose without exhibiting any malicious or high-risk behaviors. Its functionality is transparent and relies on user-configured external components for sensitive operations like API key handling and external communication.