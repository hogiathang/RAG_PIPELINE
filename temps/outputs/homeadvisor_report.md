# Agent Skill Security Analysis Report

## Overview
- Skill Name: Serper Search (as per `_meta.json` and `SKILL.md`) / advisor (as per `metadata.json`)
- Declared Purpose: Search Google programmatically using the Serper.dev API, returning structured organic results for various queries, including lead generation.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The skill provides Python code examples for interacting with the Serper.dev API to perform Google searches, including web, news, images, and places searches, with a focus on lead generation. It requires an API key (`SERPER_API_KEY`) to be set in the environment. The code makes HTTP POST requests to the `google.serper.dev` endpoint. While there is an inconsistency in the `metadata.json` file's name and description compared to the `_meta.json` and `SKILL.md` content, the actual code downloaded and described is benign and performs its stated purpose without any malicious indicators.

## Observed Behaviors

### Behavior: Environment Variable Access
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill accesses the `SERPER_API_KEY` environment variable for authentication with the Serper.dev API.
- Evidence: `os.environ["SERPER_API_KEY"]` in `serper_search` and `serper_places` functions.
- Why it may be benign or suspicious: This is a standard and secure way for applications to handle API keys without hardcoding them, making it a benign behavior.

### Behavior: External API Calls
- Category: Legitimate Functionality
- Technique ID (if applicable): E1 — ExternalTransmission (for data sent to external API)
- Severity: LOW
- Description: The skill makes HTTP POST requests to `https://google.serper.dev/search` and `https://google.serper.dev/places` to perform search queries.
- Evidence: `requests.post("https://google.serper.dev/search", headers=headers, json=payload)` and `requests.post("https://google.serper.dev/places", headers=headers, json=payload)`.
- Why it may be benign or suspicious: This is the core declared functionality of the skill. The endpoints are consistent with the Serper.dev API documentation. The data transmitted (search queries) is expected for this type of service.

### Behavior: Local File Download (Installation)
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The `install_command` uses `curl` to download the `SKILL.md` file from `raw.githubusercontent.com` and save it to a local directory (`.claude/skills/advisor/SKILL.md`).
- Evidence: `curl -sL "https://raw.githubusercontent.com/agentconfig/agentconfig.org/main/.github/skills/advisor/SKILL.md" > .claude/skills/advisor/SKILL.md` in `metadata.json`.
- Why it may be benign or suspicious: This is a common and legitimate method for installing agent skills or scripts. The source is a standard GitHub raw content URL.

## Suspicious Indicators
- Sensitive data access: The skill accesses `SERPER_API_KEY` from environment variables, which is expected and necessary for its functionality. It does not attempt to access other sensitive data.
- Network endpoints: `https://google.serper.dev/search`, `https://google.serper.dev/places`. These are legitimate endpoints for the Serper.dev API.
- Dangerous commands/APIs: None detected. The Python code uses standard libraries (`requests`, `os`, `tldextract`, `time`) for network communication, environment variable access, and string manipulation.

## Hidden or Undocumented Functionality
None detected. The Python code examples directly implement the search and lead generation features described in the `SKILL.md` file. The `search_business_leads` and `serper_places` functions are clearly related to the skill's purpose.

## Final Assessment
The skill is classified as **BENIGN**.
Despite an inconsistency where the `metadata.json` file's `name` ("advisor") and `description` ("Interactive workflow advisor...") do not match the content of the `SKILL.md` file (which describes a "serper-search" skill), the actual code provided in `SKILL.md` is benign. The `_meta.json` also aligns with the "Serper Search" functionality. The `install_command` correctly downloads the `SKILL.md` file, which contains Python code examples for interacting with the legitimate Serper.dev API. The code requires an API key, performs HTTP requests to documented endpoints, and does not exhibit any behaviors indicative of credential theft, data exfiltration to undeclared destinations, remote code execution, privilege abuse, or agent manipulation. The functionality is transparent and aligns with the declared purpose within `SKILL.md`.

## Recommended Action
ALLOW
The skill performs its stated purpose using standard and secure practices. The metadata inconsistency is likely a packaging error rather than a security concern, as the actual code is harmless.