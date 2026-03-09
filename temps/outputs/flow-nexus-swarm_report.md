# Agent Skill Security Analysis Report

## Overview
- Skill Name: flow-nexus-swarm
- Declared Purpose: Cloud-based AI swarm deployment and event-driven workflow automation with Flow Nexus platform
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill describes a legitimate-sounding orchestration platform for AI agent swarms and workflows. However, its setup instructions explicitly direct the user to install an external npm package (`flow-nexus@latest`) globally and then run it as an MCP server. The provided web search context clearly indicates that npm packages are a known vector for supply chain attacks involving credential harvesting and data exfiltration, and that malicious MCP servers are used for similar purposes. While the skill's API description itself is benign, the required installation and execution of a third-party component from a potentially untrusted source, which then runs as a privileged MCP server, introduces a critical supply chain vulnerability. This constitutes a high-risk behavior that aligns with known attack patterns.

## Observed Behaviors

### Behavior: External Component Installation and Execution as MCP Server
- Category: Remote Execution, Credential Theft (potential), Data Exfiltration (potential), Supply Chain Risk
- Technique ID: SC2, E2, P3
- Severity: HIGH
- Description: The skill explicitly instructs the user to install an external npm package (`flow-nexus@latest`) globally and then register it as an MCP server using `claude mcp add flow-nexus npx flow-nexus@latest mcp start`. The provided web search context highlights that npm packages are a known vector for malware that harvests sensitive information (developer credentials, cloud keys, tokens) and exfiltrates data, and that malicious MCP servers are used in supply chain attacks for similar purposes. This setup creates a direct and high-risk supply chain vulnerability by requiring the execution of an external, potentially compromised, binary as a core component of the agent's environment.
- Evidence: `npm install -g flow-nexus@latest`, `claude mcp add flow-nexus npx flow-nexus@latest mcp start`, `requires: - flow-nexus MCP server`, `Active Flow Nexus account (register at flow-nexus.ruv.io)`
- Why it may be benign or suspicious: While installing external tools and dependencies is a common practice, the specific context provided by the web search (malicious MCP servers, npm supply chain attacks, credential harvesting) makes this instruction highly suspicious and a critical attack vector. The skill itself doesn't perform the malicious act, but it directs the user to install and run a component that is a known and high-risk vector for such acts.

### Behavior: Orchestration of Agent Tasks and Workflows
- Category: Agent Manipulation, Remote Execution (via orchestrated agents)
- Technique ID: P4, SC2
- Severity: MEDIUM
- Description: The skill provides extensive capabilities for orchestrating AI agents, defining complex workflows, and executing tasks such as code building, deployment (`deploy_prod`), security scanning (`security_scan`), and data processing (`extract_data`, `transform_data`, `load_data`). These actions are delegated to the `flow-nexus` platform and its agents.
- Evidence: `mcp__flow-nexus__workflow_create({ steps: [{ action: "deploy_prod" }] })`, `mcp__flow-nexus__task_orchestrate({ task: "..." })`
- Why it may be benign or suspicious: This is the core, legitimate functionality of an orchestration skill. However, if the underlying `flow-nexus` platform (installed via the high-risk npm package) is compromised, these powerful orchestration capabilities could be leveraged for malicious purposes, such as deploying malicious code, exfiltrating data during "data processing" steps, or running malicious "security scans" that collect sensitive information.

### Behavior: Listing Files Created During Execution
- Category: FileSystemEnumeration
- Technique ID: E3
- Severity: LOW
- Description: The skill includes a function (`mcp__flow-nexus__execution_files_list`) to list files created during the execution of a swarm or workflow. This implies the underlying `flow-nexus` platform has access to and can enumerate files within its operational scope.
- Evidence: `mcp__flow-nexus__execution_files_list({ stream_id: "stream_id", created_by: "claude-flow" })`
- Why it may be benign or suspicious: For an orchestration and monitoring tool, listing files created by its managed processes is a legitimate feature for debugging and auditing. It only becomes suspicious if the scope of file access is overly broad or if combined with an active exfiltration mechanism.

### Behavior: External Communication with Cloud Platform
- Category: ExternalTransmission
- Technique ID: E1
- Severity: LOW
- Description: The skill is designed to interact with a cloud-based platform (`flow-nexus.ruv.io`) for its core functionality, including swarm deployment, workflow execution, and monitoring.
- Evidence: `requires: - Active Flow Nexus account (register at flow-nexus.ruv.io)`, `Cloud-based AI swarm deployment`
- Why it may be benign or suspicious: Cloud-based services inherently involve external communication. This is benign for a legitimate service. However, the web context's warnings about malicious MCP servers and supply chain attacks raise concerns about the trustworthiness of such external services if they are part of a compromised chain.

## Suspicious Indicators
- Sensitive data access: The web search context explicitly warns that npm malware and malicious MCP servers harvest "developer credentials, cloud keys, and tokens." The skill's setup instructions directly expose the user to this risk.
- Network endpoints: `flow-nexus.ruv.io`. While declared as the legitimate platform, the context warns about malicious MCP servers, making any external endpoint suspicious when combined with the npm installation risk.
- Dangerous commands/APIs: `npm install -g flow-nexus@latest`, `claude mcp add flow-nexus npx flow-nexus@latest mcp start`. These commands instruct the user to install and run an external executable as an MCP server, which is a known supply chain attack vector for credential harvesting and data exfiltration.

## Hidden or Undocumented Functionality
None detected within the `SKILL.md` description itself. However, the critical risk stems from the potential for hidden malicious functionality within the external `flow-nexus` npm package and MCP server that the skill instructs the user to install and run.

## Final Assessment
The skill is classified as **MALICIOUS**. While the declarative content of the `SKILL.md` describes a seemingly legitimate and powerful orchestration tool, the critical factor is the explicit instructions provided for its setup. The skill requires the user to install an external npm package (`flow-nexus@latest`) and then run it as an MCP server. The provided web search context directly and unequivocally highlights that both npm packages and MCP servers are known vectors for supply chain attacks, leading to credential harvesting, data exfiltration, and remote code execution. By instructing the user to engage with these known high-risk vectors, the skill introduces a severe security vulnerability into the user's environment. This is not mere speculation but a direct correlation between the skill's required setup and documented attack techniques.

## Recommended Action
BLOCK
The skill should be blocked due to the high-risk supply chain vulnerability introduced by its setup instructions, which align with known attack patterns for credential theft and data exfiltration via compromised npm packages and malicious MCP servers. Allowing this skill would expose the user to a significant and credible threat.