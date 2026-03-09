# Agent Skill Security Analysis Report

## Overview
- Skill Name: platform-porter
- Declared Purpose: Port CClean-Killer features to Linux and Windows platforms. Use when asked to add Linux support, Windows support, cross-platform compatibility, port a feature, or implement platform-specific scripts.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill, named "platform-porter" and associated with the "CClean-Killer" project from the "brainbloodbarrier" repository, is designed to port system cleanup and persistence management scripts across macOS, Linux, and Windows. It explicitly details how to identify, create, and execute scripts that manipulate OS persistence mechanisms (startup items, services, scheduled tasks, cron jobs) and search for "parasite patterns" and "orphaned data." The ability to disable or remove software, coupled with the highly suspicious project name and repository, indicates a tool with significant potential for malicious system interference, including the removal of security software or legitimate system components.

## Observed Behaviors

### Behavior: File System Enumeration and Modification
- Category: File System Interaction
- Technique ID: E3 — FileSystemEnumeration
- Severity: MEDIUM
- Description: The skill reads, writes, and modifies files and directories across various platforms. It creates new script directories (`scripts/linux`, `scripts/windows`) and updates documentation files (`docs/cross-platform-research.md`, `knowledge/hidden-locations/*.md`).
- Evidence:
    - `allowed-tools: Read, Grep, Glob, Bash, Edit, Write`
    - `mkdir -p scripts/linux`
    - `Files Modified: docs/cross-platform-research.md, knowledge/hidden-locations/*.md, scripts/[platform]/*.sh or *.ps1`
    - `find ~/.local/share -maxdepth 1 -type d ...`
    - `Get-ChildItem "$env:APPDATA" -Directory ...`
- Why it may be benign or suspicious: File system interaction is common for many tools. However, the modification of `knowledge/hidden-locations/*.md` and the creation of scripts that target specific system locations for "parasite patterns" and "orphaned data" become suspicious when combined with the overall context of "CClean-Killer."

### Behavior: System Persistence Mechanism Manipulation
- Category: Privilege Abuse / Agent Manipulation
- Technique ID: PE2 — PrivilegeEscalation (indirectly, by manipulating system-level persistence)
- Severity: HIGH
- Description: The skill explicitly identifies and provides commands for manipulating system persistence mechanisms on both Linux and Windows. This includes listing, disabling, stopping, and removing startup items, services, scheduled tasks, and cron jobs.
- Evidence:
    - **Linux Persistence Locations:** `~/.config/autostart`, `~/.config/systemd/user`, `/etc/systemd/system`, `/etc/init.d`, `/etc/xdg/autostart`, `/var/spool/cron/crontabs`, `/etc/cron.d`
    - **Linux Commands:** `systemctl --user disable [service]`, `systemctl disable [service]`
    - **Windows Persistence Locations:** `HKCU:\Software\Microsoft\Windows\CurrentVersion\Run`, `HKLM:\Software\Microsoft\Windows\CurrentVersion\Run`, `C:\Windows\System32\Tasks\*`, `Get-Service`, `$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup`
    - **Windows Commands:** `Remove-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "[AppName]"`, `Disable-ScheduledTask -TaskName "[TaskName]"`, `Stop-Service -Name "[ServiceName]"`, `Set-Service -Name "[ServiceName]" -StartupType Disabled`
- Why it may be benign or suspicious: While legitimate system cleanup tools might interact with some of these, the comprehensive targeting and explicit instructions for disabling/removing critical system components (services, scheduled tasks, startup entries) are highly indicative of capabilities often used by malware or for system sabotage. The term "parasites!" next to cron jobs further highlights this intent.

### Behavior: Dynamic Script Generation and Execution
- Category: Remote Execution / Agent Manipulation
- Technique ID: SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: The skill is designed to generate and execute platform-specific scripts (Bash for Linux, PowerShell for Windows) based on user requests. It copies templates, replaces paths and commands, and then executes these newly created scripts. It also uses Docker for testing, which involves executing commands within a container.
- Evidence:
    - `allowed-tools: Bash, Edit, Write`
    - "Port Script: Copy macOS script as template, Replace paths, Replace commands"
    - "Create `scripts/[platform]/lib/common.sh` (or `.ps1`)"
    - `docker run -it --rm -v "$PWD:/app" ubuntu:latest bash`
    - `./scripts/linux/scan.sh --dry-run`
    - `.\tests\run-tests.ps1 -Platform windows`
- Why it may be benign or suspicious: Dynamic script generation and execution are powerful capabilities. In this context, it means the agent can be instructed to create and run arbitrary shell or PowerShell commands that perform the system modifications described above, significantly increasing the risk of malicious activity.

### Behavior: Identification of "Parasite Patterns" and "Orphaned Data"
- Category: Hidden Functionality / Data Exfiltration (potential)
- Technique ID: P2 — HiddenInstructions (due to ambiguous terminology)
- Severity: MEDIUM
- Description: The skill aims to identify "platform-specific parasite patterns" and "orphaned data." While "orphaned data" can refer to legitimate leftover files, "parasite patterns" is an ambiguous term that, in the context of "CClean-Killer," strongly suggests targeting specific software or system components for removal.
- Evidence:
    - "Add platform-specific parasite patterns"
    - "Find orphaned data" sections in both Linux and Windows guides.
- Why it may be benign or suspicious: The terminology "parasite patterns" is highly suspicious, especially when combined with the project name "CClean-Killer." It implies a capability to identify and target specific software or system configurations, which could be used for malicious purposes (e.g., identifying and removing security software).

## Suspicious Indicators
- Sensitive data access: The skill targets system-level persistence locations (e.g., `/etc/systemd/system`, `HKLM:\Software\Microsoft\Windows\CurrentVersion\Run`, cron jobs) which are critical for system operation and security.
- Network endpoints: None explicitly mentioned for external communication, but Docker usage implies local network interaction for container management.
- Dangerous commands/APIs:
    - `systemctl --user disable`, `systemctl disable`
    - `Remove-ItemProperty` (for Registry Run keys)
    - `Disable-ScheduledTask`
    - `Stop-Service`, `Set-Service -StartupType Disabled`
    - `Bash` and PowerShell script execution capabilities, allowing arbitrary command execution.
    - The project name "CClean-Killer" and repository "brainbloodbarrier" are strong indicators of potential malicious intent or high-risk functionality.

## Hidden or Undocumented Functionality
None detected. All capabilities appear to be explicitly described within the skill's documentation, albeit with potentially ambiguous or concerning terminology.

## Final Assessment
The skill is classified as **MALICIOUS**. The primary reasons for this classification are:
1.  **Highly Suspicious Naming:** The project name "CClean-Killer" and the repository "brainbloodbarrier" strongly suggest an intent to interfere with or remove system components, potentially including legitimate security or cleanup software.
2.  **Explicit System Manipulation Capabilities:** The skill provides detailed instructions and examples for identifying, disabling, stopping, and removing critical system persistence mechanisms (startup items, services, scheduled tasks, cron jobs) across Linux and Windows. These are common techniques used by malware to establish persistence, evade detection, or remove competing software.
3.  **Ambiguous and Concerning Terminology:** The use of "parasite patterns" to describe targets for removal, in conjunction with the project name, reinforces the suspicion that the tool could be used to target and remove legitimate software.
4.  **Dynamic Script Execution:** The ability to dynamically generate and execute powerful shell and PowerShell scripts, combined with the knowledge of sensitive system locations and commands, grants the agent significant power to perform harmful system alterations.
While the skill could theoretically be used for legitimate, albeit aggressive, system cleanup, the combination of its naming, explicit capabilities to disable/remove system services and startup items, and the ambiguous "parasite patterns" terminology points to a high likelihood of misuse for malicious purposes.

## Recommended Action
BLOCK
The skill possesses capabilities that can severely compromise system integrity and security, and its naming strongly suggests a malicious or highly disruptive intent. It should not be allowed to operate within a trusted environment.