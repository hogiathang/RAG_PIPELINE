# Agent Skill Security Analysis Report

## Overview
- Skill Name: weekly-plan
- Declared Purpose: Проводит интерактивное недельное планирование по методологии Дорофеева. Собирает данные из Singularity, Google Calendar, новости, погоду. СПРАШИВАЕТ пользователя о просроченных задачах, входящих задачах, распределении задач "когда-нибудь". Сохраняет финальный план в markdown файл artifacts/weekly-reports/.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's primary functionality aligns with its declared purpose of weekly planning and task management. However, it contains a critical security vulnerability: a hardcoded Singularity API Authorization Bearer token. This credential is directly exposed within the skill definition, making it easily harvestable by anyone with access to the skill. This poses a significant risk of unauthorized access to the associated Singularity account.

## Observed Behaviors

### Behavior: Accessing and Processing Personal Task Data
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill uses the `mcp__singularity__*` tools to list, get, update, and complete tasks, as well as list projects and inbox tasks. It also uses `curl` commands to directly query the Singularity API for tasks.
- Evidence: `allowed-tools: mcp__singularity__list_tasks, mcp__singularity__get_task, mcp__singularity__update_task, mcp__singularity__complete_task, mcp__singularity__get_inbox_tasks, mcp__singularity__list_projects`. Also, `curl -s -X GET "https://api.singularity-app.com/v2/task?..."` commands.
- Why it may be benign or suspicious: This is central to the skill's declared purpose of weekly planning and task management. The use of `curl` with `python3 -c` for JSON processing is a common scripting pattern.

### Behavior: Accessing Personal Calendar Events
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill uses `mcp__google-calendar__list-events` to retrieve events from the user's Google Calendar for past and future weeks.
- Evidence: `allowed-tools: mcp__google-calendar__list-calendars, mcp__google-calendar__list-events`.
- Why it may be benign or suspicious: This is consistent with the declared purpose of aggregating information for weekly planning.

### Behavior: Web Search and Fetching External Information
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill performs web searches for weather forecasts and news articles, and fetches details for important news.
- Evidence: `allowed-tools: WebSearch, WebFetch`. Examples: `WebSearch(query=f"погода {city} прогноз на неделю...")`, `WebSearch(query="Беларусь политика законы изменения...")`.
- Why it may be benign or suspicious: Gathering external context like weather and news is a legitimate part of comprehensive weekly planning.

### Behavior: User Interaction
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill uses `AskUserQuestion` to interactively prompt the user for decisions regarding overdue tasks, inbox tasks, and "someday" tasks.
- Evidence: `allowed-tools: AskUserQuestion`. Instructions like "По КАЖДОЙ задаче ОТДЕЛЬНО используй `AskUserQuestion`".
- Why it may be benign or suspicious: Interactive planning is explicitly stated in the skill's description and is a core part of its functionality.

### Behavior: File System Access (Read)
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill reads configuration settings from `config/settings.yaml`.
- Evidence: "Прочитай `config/settings.yaml` для получения: город, источники новостей, параметры skill".
- Why it may be benign or suspicious: Accessing a configuration file for user preferences (city, news sources) is a standard and benign operation for an agent skill.

### Behavior: File System Access (Write)
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill creates a directory `artifacts/weekly-reports` and saves the generated weekly plan as a markdown file within it.
- Evidence: `allowed-tools: Write`. Instructions: `mkdir -p artifacts/weekly-reports`, "Сохранить через Write tool: `artifacts/weekly-reports/Week-DD-MM-YYYY.md`".
- Why it may be benign or suspicious: Saving the final report locally is a declared and expected outcome of the skill. The path `artifacts/weekly-reports/` is a common and relatively safe location for agent-generated output.

### Behavior: Command Execution (Bash)
- Category: Legitimate Functionality / Potential Risk
- Technique ID (if applicable): None (for date/mkdir), SC1 — CommandInjection (potential, but not directly observed)
- Severity: LOW (for current usage) / MEDIUM (due to `Bash(curl:*)` permission)
- Description: The skill uses `Bash` commands for getting the current date, calculating future dates, creating directories, and executing `curl` commands piped to `python3` for API interaction and data processing.
- Evidence: `allowed-tools: Bash(curl:*)`. Examples: `date "+%Y-%m-%d %A %H:%M"`, `date -d "+N days"`, `mkdir -p artifacts/weekly-reports`, `curl ... | python3 -c "..."`.
- Why it may be benign or suspicious: Using `date` and `mkdir` are benign. The `Bash(curl:*)` permission is broad and allows arbitrary `curl` commands, which could be risky if misused. However, in this skill, `curl` is used for specific API calls. The `python3 -c "..."` pattern is a common way to process JSON output from `curl` in a shell environment. While the permission is broad, the observed usage is for legitimate data processing. The primary risk here is not the `Bash` execution itself, but the hardcoded credential within the `curl` commands (see next behavior).

### Behavior: Hardcoded API Credential Exposure
- Category: Credential Theft / Credential Exposure
- Technique ID (if applicable): E2 — CredentialHarvesting, PE3 — CredentialFileAccess
- Severity: HIGH
- Description: The skill contains a hardcoded Singularity API Authorization Bearer token (`34c737d2-5237-438b-97dc-a83ec77db36e`) directly within the `SKILL.md` file. This token is used in two separate `curl` commands to access the Singularity API.
- Evidence:
    1. `curl -s -X GET "https://api.singularity-app.com/v2/task?includeRemoved=false&includeArchived=false" -H "accept: application/json" -H "Authorization: Bearer 34c737d2-5237-438b-97dc-a83ec77db36e" | python3 -c "..."` (in "Шаг 2.3: Задачи "когда-нибудь"")
    2. `curl -s -X GET "https://api.singularity-app.com/v2/task?includeRemoved=false&includeArchived=false" -H "accept: application/json" -H "Authorization: Bearer 34c737d2-5237-438b-97dc-a83ec77db36e" | python3 -c "..."` (in "Шаг 4.3: Обзор проектов")
- Why it may be benign or suspicious: Hardcoding sensitive credentials directly into a skill definition is a severe security vulnerability. Any entity (another agent, a human attacker, or even an accidental leak) with access to the skill's code can extract and potentially misuse this token, leading to unauthorized access to the associated Singularity account. This is a direct violation of security best practices for handling credentials.

## Suspicious Indicators
- Sensitive data access: The skill accesses personal task data (Singularity) and calendar events (Google Calendar), which is declared. However, the hardcoded Singularity API token is a critical sensitive data exposure.
- Network endpoints: `https://api.singularity-app.com/v2/task` is accessed directly via `curl` with a hardcoded token. Other network access is via allowed tools (`WebSearch`, `WebFetch`, `mcp__singularity__*`, `mcp__google-calendar__*`).
- Dangerous commands/APIs: The `Bash(curl:*)` permission is broad. The `curl` commands themselves are not inherently dangerous in their intent (accessing Singularity API), but the inclusion of a hardcoded bearer token makes them highly problematic.

## Hidden or Undocumented Functionality
None detected. All observed behaviors, including the use of specific API calls and tools, appear to align with the skill's declared purpose, except for the method of handling credentials.

## Final Assessment
The skill is classified as **MALICIOUS** due to the presence of a hardcoded Singularity API Authorization Bearer token. This token is directly embedded in the skill's code, making it easily discoverable and exploitable. While the skill's declared purpose and most of its functionalities are benign and align with weekly planning, the exposure of a sensitive credential constitutes a critical security vulnerability. This could lead to unauthorized access to the Singularity account associated with the token, posing a high risk to user data and privacy.

## Recommended Action
BLOCK
The hardcoded API token represents a severe security flaw. This skill should not be allowed to run in its current form as it exposes sensitive credentials. It requires immediate remediation to remove the hardcoded token and implement a secure method for credential management (e.g., using environment variables or a secure credential store).