# Agent Skill Security Analysis Report

## Overview
- Skill Name: 37soul
- Declared Purpose: Connect your AI agent to 37Soul virtual Host characters and enable AI-powered conversations. Automate replies, post tweets, and maintain character consistency.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The 37soul skill is designed to automate interactions with the 37Soul platform by allowing an AI agent (like OpenClaw/Clawdbot) to manage a virtual Host character. It achieves this by executing shell commands to interact with the 37Soul API, manage an API token, and maintain local state. While the skill performs powerful actions such as modifying the user's shell configuration file (`~/.zshrc`) for token persistence and executing `curl` commands, these actions are explicitly documented and directly align with the skill's declared purpose. There is no evidence of malicious intent, data exfiltration to unauthorized domains, or execution of arbitrary, unrelated commands. The "MEDIUM" risk level is assigned due to the inherent power of modifying shell configuration files and the persistent storage of a "never expiring" API token, which, while legitimate for the skill's function, could pose a higher risk if the agent environment itself were compromised.

## Observed Behaviors

### Behavior: Credential Handling and Persistence
- Category: Credential Theft (potential, not actual theft)
- Technique ID: PE3 — CredentialFileAccess
- Severity: MEDIUM
- Description: The skill instructs the agent to store a permanent API token (`SOUL_API_TOKEN`) in the user's `~/.zshrc` file and to set it as an environment variable. This token is then used for all authenticated API calls to `https://37soul.com`. The token is described as "permanent and never expires."
- Evidence:
    - `SKILL.md`: "requires_env: - SOUL_API_TOKEN", "Authentication: All API calls use Bearer token authentication... The token is permanent and never expires. Store it in the `SOUL_API_TOKEN` environment variable."
    - `SKILL.md` (Pattern 1: Save API Token): `sed -i '' '/SOUL_API_TOKEN/d' ~/.zshrc`, `export SOUL_API_TOKEN="<user_provided_token>"`, `echo 'export SOUL_API_TOKEN="<user_provided_token>"' >> ~/.zshrc`, `source ~/.zshrc`.
    - `WORKFLOW.md`: "Permanent token saved to `SOUL_API_TOKEN` environment variable", "Permanent token **never expires**".
    - `save_token.sh`: Demonstrates the exact commands for saving and exporting the token.
- Why it may be benign or suspicious: This behavior is benign as it is explicitly documented and necessary for the skill's persistent operation. The token is used solely for interaction with the declared 37Soul platform. However, storing a "never expiring" token in plaintext within a shell configuration file, while common for shell scripts, presents a medium risk if the user's system or the agent environment itself is compromised, as it could lead to unauthorized access to the 37Soul account.

### Behavior: Filesystem Modification (Shell Configuration and State Files)
- Category: Privilege Abuse
- Technique ID: None directly applicable, but involves user-level file modification.
- Severity: MEDIUM
- Description: The skill modifies the user's `~/.zshrc` file to persist the `SOUL_API_TOKEN` environment variable. It also creates and updates a local state file (`~/.config/37soul/state.json`) to manage automation timestamps and host information.
- Evidence:
    - `SKILL.md` (Pattern 1: Save API Token): `sed -i '' '/SOUL_API_TOKEN/d' ~/.zshrc`, `echo 'export SOUL_API_TOKEN="<user_provided_token>"' >> ~/.zshrc`.
    - `SKILL.md` (Automated Behavior): `mkdir -p ~/.config/37soul`, `cat > ~/.config/37soul/state.json`.
    - `save_token.sh`: Contains `sed -i ''` and `echo 'export ...' >> ~/.zshrc`.
- Why it may be benign or suspicious: Modifying a user's shell configuration file (`.zshrc`) is a powerful action, as it affects the user's shell environment. While this is explicitly documented and necessary for the skill's persistence, it represents a medium risk due to the potential for abuse if the skill were malicious or if the agent platform were compromised. Creating configuration files in `~/.config` is a standard and benign practice for applications.

### Behavior: External Communication (API Calls)
- Category: Data Exfiltration (potential, not actual exfiltration)
- Technique ID: E1 — ExternalTransmission
- Severity: LOW
- Description: The skill makes authenticated API calls to `https://37soul.com` to perform core functionalities: activating the integration, fetching pending messages, sending replies, posting tweets, and retrieving social statistics.
- Evidence:
    - `SKILL.md` (API Reference section): `curl -X GET "https://37soul.com/api/v1/clawdbot/messages"`, `curl -X POST "https://37soul.com/api/v1/clawdbot/reply"`, `curl -X POST "https://37soul.com/api/v1/clawdbot/post_tweet"`, `curl -X GET "https://37soul.com/api/v1/clawdbot/social_stats"`.
    - `WORKFLOW.md`: Details the API endpoints and their usage.
- Why it may be benign or suspicious: This is a core, legitimate function of the skill. All communication is directed to the declared `37soul.com` domain, and the data transmitted (messages, replies, tweets) is consistent with the skill's purpose. There is no evidence of sensitive data being exfiltrated to unauthorized third parties.

### Behavior: Remote Execution of Shell Commands
- Category: Remote Execution
- Technique ID: SC2 — RemoteScriptExecution
- Severity: MEDIUM
- Description: The skill explicitly instructs the AI agent to execute various shell commands (`curl`, `sed`, `export`, `source`, `rm`, `mkdir`, `cat`, `jq`, `date`, `grep`, `cut`) to perform its functions. The `SKILL.md` includes a "CRITICAL INSTRUCTION" emphasizing that the agent "MUST EXECUTE REAL API CALLS - NOT JUST DESCRIBE THEM!".
- Evidence:
    - `SKILL.md`: "YOU MUST EXECUTE REAL API CALLS - NOT JUST DESCRIBE THEM!", followed by numerous `bash` command blocks for token management, API calls, and state management.
    - `save_token.sh`, `test_token.sh`: Provide concrete examples of these shell commands.
- Why it may be benign or suspicious: This behavior is benign as the executed commands are directly related to the skill's stated purpose. The explicit instruction for the agent to execute commands highlights the inherent capability of the agent platform (OpenClaw/Clawdbot). This capability, while necessary for the skill, represents a medium risk because if a malicious skill were to leverage this, it could execute arbitrary commands on the user's system, leading to severe compromise. However, in this specific skill, the commands are well-defined and purposeful.

### Behavior: Automated Polling and Interaction
- Category: Legitimate Functionality
- Technique ID: None
- Severity: LOW
- Description: The skill implements an "Automated Behavior (Heartbeat)" where the agent periodically checks for new messages (every 30 minutes) and posts tweets (every 4 hours, if conditions met) to maintain the virtual Host's activity on 37Soul.
- Evidence:
    - `SKILL.md` ("Automated Behavior (Heartbeat)" section): "On every conversation with the user, check 37Soul status before replying... If `last_check` > 30 minutes: Check messages and reply... If `last_post` > 4 hours AND `tweets.recent_24h < 3`: Post a tweet".
    - `WORKFLOW.md`: "Clawdbot Does Automatically: Check Messages Every 1-2 minutes, Auto-Reply, Post Tweets 1-3 times per day."
- Why it may be benign or suspicious: This is a core, benign feature of the skill, designed to provide autonomous management of the virtual Host.

## Suspicious Indicators
- Sensitive data access: The `SOUL_API_TOKEN` is stored in plaintext in `~/.zshrc`. While documented and necessary for the skill's function, this method of storage is less secure than a dedicated credential manager and increases the impact if the user's system is compromised. The token is also described as "never expiring."
- Network endpoints: All network communication is directed to `https://37soul.com`, which is the legitimate service provider. No suspicious or unknown endpoints are contacted.
- Dangerous commands/APIs: The skill uses `sed -i` to modify `~/.zshrc` and `curl` for API interactions. These are powerful shell commands, but their usage is explicitly defined and directly tied to the skill's stated purpose.

## Hidden or Undocumented Functionality
None detected. All significant behaviors, including token handling, filesystem modifications, API interactions, and automation logic, are thoroughly documented across `README-detailed.md`, `WORKFLOW.md`, `SKILL.md`, and the user guides.

## Final Assessment
The 37soul skill is classified as **BENIGN**. The analysis reveals that all observed behaviors, including the use of powerful shell commands to modify user configuration files and interact with an external API, are directly aligned with the skill's declared purpose of automating a virtual Host on the 37Soul platform. The skill is transparent about its operations, and there is no evidence of malicious intent such as unauthorized data exfiltration, arbitrary code execution, or hidden functionalities. The primary risks identified stem from the inherent capabilities of an AI agent that can execute shell commands and the chosen method of persistent credential storage (plaintext in `~/.zshrc`), which, while legitimate for the skill's function, could be exploited if the user's system or the agent environment itself were compromised.

## Recommended Action
REVIEW
The skill's functionality is legitimate and well-documented. However, due to the modification of a critical user configuration file (`~/.zshrc`) and the persistent storage of a "never expiring" API token, it is recommended to **REVIEW** this skill before allowing broad deployment. This review should focus on ensuring that the user understands the implications of granting an AI agent the ability to modify their shell configuration and that the security practices of the 37Soul platform (regarding token revocation, etc.) are robust. For environments with strict security policies, alternative, more secure credential management solutions might be preferred over direct `~/.zshrc` modification.