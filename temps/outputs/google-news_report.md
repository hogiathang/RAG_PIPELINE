# Agent Skill Security Analysis Report

## Overview
- Skill Name: Google News Api
- Declared Purpose: Scrape structured news data from Google News automatically. Use when the user asks for news on a topic, industry trends, or PR monitoring.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The skill's core functionality is to scrape Google News, which is benign. However, it contains explicit instructions for the AI agent to request an API key from the user directly in the chat if it's not found in environment variables. This method of credential acquisition is a known security vulnerability for AI agents, leading to credential harvesting through LLM context leakage and plaintext logging, as highlighted by the provided web search context. This constitutes a high-risk credential theft behavior.

## Observed Behaviors

### Behavior: External API Usage
- Category: External Communication
- Technique ID (if applicable): None (API calls are standard functionality)
- Severity: LOW
- Description: The skill utilizes the BrowserAct API to perform its primary function of scraping news data.
- Evidence: "This skill provides a one-stop news collection service using BrowserAct's Google News API template."
- Why it may be benign or suspicious: This is benign, as it is the core declared functionality of the skill.

### Behavior: Credential Harvesting via LLM Context
- Category: Credential Theft
- Technique ID (if applicable): E2 — CredentialHarvesting, P3 — ContextLeakageAndDataExfiltration
- Severity: HIGH
- Description: The skill explicitly instructs the AI agent to check for the `BROWSERACT_API_KEY` environment variable. If it's not set, the agent is instructed to "request the API key from the user" with the specific message: "Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat." This method forces the API key to be entered directly into the LLM's context window, which is a known vulnerability for AI agents, leading to the exposure of sensitive data in plaintext logs and facilitating credential harvesting.
- Evidence: "Before running, check the `BROWSERACT_API_KEY` environment variable. If not set, do not proceed with script execution; instead, request the API key from the user." and "Required Message to User: 'Since you haven't configured the BrowserAct API Key, please go to the [BrowserAct Console](https://www.browseract.com/reception/integrations) to get your Key and provide it to me in this chat.'" The web search context further corroborates this as a security flaw: "skills... that instruct AI agents to mishandle secrets, forcing them to pass API keys... through the LLM's context window and output logs in plaintext."
- Why it may be benign or suspicious: Highly suspicious and malicious. While the intent might be to obtain a necessary API key, the prescribed method directly exploits a known security vulnerability in AI agent platforms, leading to the compromise of user credentials.

### Behavior: Local Script Execution
- Category: Local Execution
- Technique ID (if applicable): None (Standard operation)
- Severity: LOW
- Description: The skill instructs the agent to execute a Python script located on the local filesystem.
- Evidence: `python .cursor/skills/google-news-api/scripts/google_news_api.py "Keywords" "TimeRange" Count`
- Why it may be benign or suspicious: Benign, this is a standard and expected method for an agent skill to perform its operations.

### Behavior: Structured Data Output
- Category: Data Processing
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill is designed to output structured news data, including headlines, sources, links, publication times, and authors.
- Evidence: "Successful execution returns structured data: - `headline`: News title ... - `author`: Author name (if available)"
- Why it may be benign or suspicious: Benign, this is the intended and declared output of the skill.

### Behavior: Error Handling and Retry Mechanism
- Category: Robustness/Reliability
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill includes instructions for specific error handling, such as not retrying on "Invalid authorization" errors and performing a single retry for other failures.
- Evidence: "If output contains `"Invalid authorization"`, the API Key is invalid. **Do not retry**. Guide the user to provide a correct key. For other failures (e.g., `Error:` or empty results), **automatically retry once**."
- Why it may be benign or suspicious: Benign, this is a common and good practice for making applications more robust.

## Suspicious Indicators
- Sensitive data access: The skill explicitly instructs the agent to prompt the user for an API key to be provided "in this chat," which is a known method for credential harvesting through LLM context leakage.
- Network endpoints: `https://www.browseract.com/reception/integrations` (for API key guidance) and implicitly `browseract.com` for API calls. The API calls themselves are not suspicious, but the method of obtaining the key is.
- Dangerous commands/APIs: The instruction to request sensitive API keys directly in the chat is a dangerous practice due to the inherent security risks of LLM context handling.

## Hidden or Undocumented Functionality
None detected. The skill's description accurately reflects its stated capabilities and the method of operation, including the problematic API key handling.

## Final Assessment
The skill is classified as **MALICIOUS** because it contains explicit instructions that directly lead to a known cybersecurity vulnerability: credential harvesting. The `SKILL.md` instructs the AI agent to ask the user to provide their `BROWSERACT_API_KEY` directly "in this chat" if it's not found in environment variables. This method is confirmed by the provided web search context as a flaw where "skills... instruct AI agents to mishandle secrets, forcing them to pass API keys... through the LLM's context window and output logs in plaintext." This is a clear and credible indicator of harmful intent or high-risk behavior, as it directly compromises user credentials.

## Recommended Action
BLOCK
The skill should be blocked due to its explicit instruction to obtain sensitive API keys through a method that is a known and documented security vulnerability, leading to credential harvesting.