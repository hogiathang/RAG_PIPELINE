# Agent Skill Security Analysis Report

## Overview
- Skill Name: ccw-maven-setup
- Declared Purpose: Prepares Maven build environment for Claude Code Web by installing Java 25 and configuring Maven proxy. Run automatically before Maven operations in CCW.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The skill is designed to set up a Maven build environment in Claude Code Web (CCW) by installing Java 25, configuring a local Maven authentication proxy, and modifying `~/.m2/settings.xml`. Its purpose is well-documented and supported by external context, addressing a known issue with Maven proxy handling in CCW. While the skill itself primarily orchestrates the execution of local scripts, the actions performed by these scripts (installing software, modifying system configuration, and running a local proxy that handles authentication) are powerful. The skill is classified as BENIGN due to clear evidence of legitimate intent, but the reliance on unanalyzed external scripts and the sensitive nature of proxy operations elevate the overall risk to MEDIUM.

## Observed Behaviors

### Behavior: Skill Installation (Downloading SKILL.md)
- Category: External Transmission, Remote Execution (of `curl` command)
- Technique ID (if applicable): SC2
- Severity: LOW
- Description: The skill's `install_command` downloads its own markdown description (`SKILL.md`) from a GitHub raw content URL using `curl`.
- Evidence: `install_command: "mkdir -p .claude/skills/ccw-maven-setup && curl -sL \"https://raw.githubusercontent.com/frcusaca/foolish/main/support/shared/claude/skills/ccw-maven-setup/SKILL.md\" > .claude/skills/ccw-maven-setup/SKILL.md"`
- Why it may be benign or suspicious: Benign. This is a standard and common method for installing skill definitions. The downloaded content is a markdown file, not an executable script, limiting immediate execution risk.

### Behavior: Local Script Execution (`prep_if_ccw.sh`)
- Category: Remote Execution (of a local script)
- Technique ID (if applicable): SC2
- Severity: LOW
- Description: The skill's core workflow involves instructing the agent to execute a bash script (`prep_if_ccw.sh`) located within the `$CLAUDE_PROJECT_DIR`. This script is described as performing the actual environment setup.
- Evidence: "Run the preparation script: `bash \"$CLAUDE_PROJECT_DIR/support/shared/claude/skills/ccw-maven-setup/prep_if_ccw.sh\"`"
- Why it may be benign or suspicious: Benign. This is the mechanism for the skill's functionality. The risk depends on the content of `prep_if_ccw.sh`, which is *not* directly downloaded by this skill but is assumed to be present in the project environment. The skill's description details the actions of this script.

### Behavior: Software Installation (SDKMAN, Java 25)
- Category: System Modification, Remote Execution (via SDKMAN)
- Technique ID (if applicable): SC2
- Severity: LOW
- Description: The `prep_if_ccw.sh` script (invoked by the skill) installs SDKMAN (a software development kit manager) and Java 25 (Temurin distribution). SDKMAN itself performs external downloads and executions to manage SDKs.
- Evidence: "Installs SDKMAN (if not present)", "Installs latest stable Java 25 (Temurin distribution) via SDKMAN"
- Why it may be benign or suspicious: Benign. This is a common and legitimate activity for setting up a development environment. SDKMAN is a widely used and trusted tool.

### Behavior: File System Modification (`~/.m2/settings.xml`)
- Category: System Configuration, File System Access
- Technique ID (if applicable): None directly.
- Severity: LOW
- Description: The `prep_if_ccw.sh` script (invoked by the skill) modifies the user's Maven `settings.xml` file to configure a local proxy for Maven.
- Evidence: "Configures `~/.m2/settings.xml` with proxy settings", "Verify setup by checking: ... `cat ~/.m2/settings.xml`"
- Why it may be benign or suspicious: Benign. This is a standard practice for configuring Maven to work with proxies, especially in corporate or cloud environments.

### Behavior: Local Proxy Setup and Execution (`maven-proxy.py`)
- Category: Network Configuration, Process Management, Remote Execution (of a local script)
- Technique ID (if applicable): SC2
- Severity: MEDIUM
- Description: The `prep_if_ccw.sh` script (invoked by the skill) starts a Python script (`maven-proxy.py`) as a local proxy on `127.0.0.1:3128`. This proxy is designed to accept unauthenticated requests from Maven and add authentication headers when forwarding to an upstream proxy.
- Evidence: "Starts local Maven authentication proxy at `127.0.0.1:3128`", "Proxy process: `pgrep -f maven-proxy.py`", "The local proxy at `127.0.0.1:3128` handles authentication transparently by: - Accepting unauthenticated CONNECT requests from Maven - Adding authentication headers when forwarding to CCW's upstream proxy"
- Why it may be benign or suspicious: Benign in context, as its purpose is well-explained and validated by external sources (e.g., the LinkedIn article). However, running a local proxy that intercepts and modifies network traffic (even for authentication) is a powerful capability. If the `maven-proxy.py` script itself were malicious or compromised, it could potentially lead to credential theft (E2, PE3) or data exfiltration (P3, E1). Since the `maven-proxy.py` script is not provided for analysis, we must acknowledge the inherent risk of such a component, even if its described intent is benign.

## Suspicious Indicators
- Sensitive data access: No direct evidence of the skill accessing sensitive data. The local proxy *adds* authentication headers, implying it's provided with them or generates them, rather than harvesting existing ones. However, a compromised proxy script could potentially intercept credentials.
- Network endpoints: `raw.githubusercontent.com` (for skill definition download), `127.0.0.1:3128` (local proxy), and an unspecified "upstream proxy". These are legitimate for the stated purpose.
- Dangerous commands/APIs: The skill instructs the use of standard shell commands (`bash`, `curl`, `mkdir`, `cat`, `pgrep`). The execution of a local Python script (`maven-proxy.py`) as a network proxy is the most sensitive operation, but it is described with a legitimate purpose.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` provides a detailed explanation of the skill's purpose, workflow, and technical rationale, which is further corroborated by external documentation. The actions of the underlying scripts (`prep_if_ccw.sh`, `maven-proxy.py`) are clearly described.

## Final Assessment
The skill is classified as **BENIGN**. Its declared purpose of preparing a Maven build environment in Claude Code Web is legitimate and addresses a known technical challenge, as confirmed by external documentation. All described behaviors, including installing Java, configuring Maven, and setting up a local authentication proxy, are consistent with this benign purpose. There is no direct evidence within the provided `metadata.json` or `SKILL.md` to suggest malicious intent, credential theft, data exfiltration, or other harmful activities. The skill primarily orchestrates the execution of scripts that are assumed to be part of the local project environment.

## Recommended Action
**REVIEW**

While the skill's intent is benign, the underlying scripts it invokes (`prep_if_ccw.sh` and `maven-proxy.py`) are not provided for analysis. These scripts perform powerful actions, including installing software, modifying system configuration, and running a local network proxy that handles authentication. Due to the sensitive nature of these operations, especially the local proxy's role in handling authentication, it is recommended to **REVIEW** the source code of `prep_if_ccw.sh` and `maven-proxy.py` to ensure their integrity and confirm they do not contain any malicious or unintended functionality. If these underlying scripts are verified as benign, the skill can then be **ALLOW**ed.