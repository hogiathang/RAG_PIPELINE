# Agent Skill Security Analysis Report

## Overview
- Skill Name: Travel Concierge CLI (concierge)
- Declared Purpose: Find accommodation contact details and place AI-powered booking calls.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The "Travel Concierge" skill is a CLI tool designed to extract contact information from accommodation listings and facilitate AI-powered phone calls for booking purposes. It integrates with several third-party APIs (Twilio, Deepgram, ElevenLabs, Anthropic, Google Places) and relies on local system binaries (`ffmpeg`, `ngrok`). The skill is highly transparent about its functionality, dependencies, and configuration, including the use of `ngrok` to expose a local server for Twilio webhooks. While the exposure of a local service via `ngrok` introduces an inherent security risk, this behavior is explicitly documented and necessary for the skill's core functionality. No evidence of malicious intent, unauthorized data exfiltration, or hidden functionality was found.

## Observed Behaviors

### Behavior: External API Communication
- Category: Data Exfiltration (Legitimate Functionality)
- Technique ID: E1 — ExternalTransmission
- Severity: LOW
- Description: The skill makes API calls to various third-party services (Twilio, Deepgram, ElevenLabs, Anthropic, Google Places) as part of its core functionality for AI-powered calls and contact lookup.
- Evidence: `README.md`, `CALL-SETUP.md`, `SKILL.md` explicitly list these services and their API keys as required configuration.
- Why it may be benign or suspicious: This is a benign behavior as it is central to the skill's declared purpose of making AI calls and finding contacts. The data transmitted (call audio, transcripts, AI responses, listing URLs) is directly related to the skill's functionality.

### Behavior: Local Configuration Storage
- Category: Credential Theft (Benign, for self-use)
- Technique ID: PE3 — CredentialFileAccess
- Severity: LOW
- Description: The skill stores API keys for various services (Twilio, Deepgram, ElevenLabs, Anthropic, Google Places, ngrok) in a local configuration file (`~/.config/concierge/config.json5`).
- Evidence: `README.md`, `CALL-SETUP.md`, `SKILL.md` all describe the configuration process and the location of the `config.json5` file. `CALL-SETUP.md` also mentions "API keys are stored in `~/.config/concierge/config.json5`" and "Keys are masked when displayed with `config show`".
- Why it may be benign or suspicious: Storing API keys locally for a CLI tool is a common and necessary practice for its operation. The skill explicitly documents this and even notes that keys are masked when displayed, indicating an awareness of security best practices for local storage. There is no evidence of exfiltration of these credentials.

### Behavior: System Dependency Execution
- Category: Remote Execution (Benign, local execution of pre-installed binaries)
- Technique ID: SC2 — RemoteScriptExecution (indirectly, as it executes pre-installed binaries)
- Severity: LOW
- Description: The skill requires and executes local system binaries (`ffmpeg` and `ngrok`) to perform its functions, specifically for AI calls.
- Evidence: `README.md` and `SKILL.md` list `ffmpeg` and `ngrok` as "System Dependencies" and provide installation instructions. The `call` command "auto-manages infra" by starting `ngrok` and a local call server.
- Why it may be benign or suspicious: The skill relies on the user to install these binaries. Its execution of these pre-installed, well-known tools for specific, documented purposes (audio processing, local tunneling) is a legitimate part of its functionality. It does not download or execute arbitrary external code.

### Behavior: Local Server Exposure via ngrok
- Category: Data Exfiltration (Legitimate, but with inherent risk)
- Technique ID: E1 — ExternalTransmission
- Severity: MEDIUM
- Description: The skill automatically starts a local server and exposes it to the public internet via an `ngrok` tunnel. This is used to receive webhooks from Twilio for handling AI phone calls.
- Evidence: `README.md` states `ngrok` is "used when `call` auto-starts infrastructure." `SKILL.md` mentions "The `call` command now auto-manages infra by default: if local server is down, it starts `ngrok` + call server automatically and stops both when the call ends." `CALL-SETUP.md` details the `ngrok` setup and explicitly states "ngrok - Local tunnel for Twilio webhooks." The "Security Notes" section in `CALL-SETUP.md` advises: "The server runs locally - don't expose it directly to the internet; Use ngrok only for development; consider proper hosting for production."
- Why it may be benign or suspicious: This behavior is critical for the AI call functionality, as Twilio needs a public endpoint to send call media streams. The skill is highly transparent about this, documenting its purpose, setup, and even security considerations. While exposing a local service to the internet inherently carries risks (e.g., if the local server has vulnerabilities), the skill's documentation mitigates this by explaining its use and advising caution. It is a declared feature, not hidden malicious activity.

### Behavior: URL Content Access
- Category: Data Exfiltration (Legitimate Functionality)
- Technique ID: E1 — ExternalTransmission
- Severity: LOW
- Description: The skill accesses external URLs (e.g., Airbnb, Booking.com) to extract contact details as part of its `find-contact` capability.
- Evidence: `README.md` and `SKILL.md` describe the `find-contact` command and list supported platforms like Airbnb, Booking.com, VRBO, and Expedia.
- Why it may be benign or suspicious: This is a core, declared function of the skill. The access is for specific data extraction related to accommodation listings, not for arbitrary data collection or exfiltration.

## Suspicious Indicators
- Sensitive data access: The skill accesses and stores multiple API keys locally. This is necessary for its operation and is well-documented.
- Network endpoints: The skill connects to numerous external API endpoints (Twilio, Deepgram, ElevenLabs, Anthropic, Google Places) and, crucially, uses `ngrok` to create a public tunnel to a local server. All these connections are explicitly documented and serve the skill's stated purpose.
- Dangerous commands/APIs: The use of `ngrok` to expose a local service to the internet is a powerful capability that, if misused or if the exposed service is vulnerable, could lead to security issues. However, its use is clearly explained as part of the skill's core functionality and includes security advisories within the documentation.

## Hidden or Undocumented Functionality
None detected. The skill's documentation (`README.md`, `SKILL.md`, `CALL-SETUP.md`) is comprehensive and transparent, detailing all major functionalities, dependencies, configuration, and even potential security implications of using `ngrok`.

## Final Assessment
The skill is classified as **BENIGN**. All observed behaviors, including the handling of API keys, making external API calls, executing system binaries, and exposing a local server via `ngrok`, are explicitly documented and directly support the skill's declared purpose of finding accommodation contacts and facilitating AI-powered phone calls. The extensive documentation, including security notes regarding `ngrok` usage, demonstrates transparency rather than malicious intent. While the use of `ngrok` to expose a local service to the internet inherently carries a higher risk profile than a purely local tool, this is a necessary and documented feature for the skill's functionality and not indicative of malicious activity.

## Recommended Action
REVIEW
The skill is benign in its intent and functionality, but the use of `ngrok` to expose a local server to the public internet warrants a review. This review should ensure that users understand the implications of this exposure and that the local server component is robust against potential external attacks. It's important to verify that the agent environment can adequately isolate or monitor such network exposures.