# Agent Skill Security Analysis Report

## Overview
- Skill Name: Metra Skill
- Declared Purpose: Real-time Chicago Metra commuter rail data for OpenClaw, including train arrivals, vehicle tracking, service alerts, schedule info, and fare calculation for all 11 Metra lines.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The Metra Skill is designed to provide real-time and static Metra commuter rail data. It fetches data from official Metra GTFS-RT (real-time) and GTFS (static) feeds, requiring a user-provided API key for real-time data. The skill clearly documents its functionality, data sources, and security/privacy practices, explicitly stating that no user data is transmitted and no telemetry is collected. All observed behaviors align with its declared purpose.

## Observed Behaviors

### Behavior: External API Calls for Real-time Data
- Category: Data Retrieval
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill makes HTTPS requests to `gtfspublic.metrarr.com` to retrieve real-time Metra trip updates, vehicle positions, and service alerts. These requests require a `METRA_API_KEY` passed as a Bearer token in the Authorization header.
- Evidence: `README.md` and `SKILL.md` explicitly list `https://gtfspublic.metrarr.com/gtfs/public/tripupdates`, `/positions`, and `/alerts` as endpoints requiring `Authorization: Bearer {METRA_API_KEY}`.
- Why it may be benign or suspicious: This is core functionality for a transit data skill. The endpoints are official Metra domains, and the API key is for authentication, not exfiltration. The use of HTTPS ensures secure transmission of the API key.

### Behavior: External Data Download for Static Data
- Category: Data Retrieval, Local File System Write
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill downloads a ZIP archive containing GTFS static schedule data from `https://schedules.metrarail.com/gtfs/schedule.zip`. This data is then extracted locally.
- Evidence: `README.md` and `SKILL.md` describe the `node scripts/metra.mjs refresh-gtfs` command, which downloads `schedule.zip` from `schedules.metrarail.com` and extracts it.
- Why it may be benign or suspicious: This is necessary for the skill to function, as it relies on static schedule data. The source URL is an official Metra domain.

### Behavior: Local File System Access and Utility Execution
- Category: Local File System Interaction, System Utility Execution
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill writes downloaded GTFS static data to `~/.metra/gtfs/` and uses the `unzip` system utility to extract the archive. It also installs Node.js dependencies using `npm install`.
- Evidence: `README.md` and `SKILL.md` specify `~/.metra/gtfs/` as the local storage location for GTFS data. `SKILL.md` lists `unzip` as a required binary. `package.json` lists `protobufjs` as a dependency, and `SKILL.md` includes an `npm install` command.
- Why it may be benign or suspicious: Writing to a user's home directory for application data is standard practice. `unzip` is a common utility for extracting archives. `npm install` is standard for Node.js dependency management. All these actions are well-documented and essential for the skill's operation.

### Behavior: Environment Variable Access
- Category: Configuration Access
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill reads the `METRA_API_KEY` from environment variables for authenticating with Metra's real-time data feeds.
- Evidence: `README.md` and `SKILL.md` provide instructions to set `METRA_API_KEY` as an environment variable and state it is required for all real-time data.
- Why it may be benign or suspicious: This is a standard and secure way to handle API keys for applications, preventing them from being hardcoded in the source.

### Behavior: Dependency on `protobufjs`
- Category: Library Usage
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill depends on the `protobufjs` library for parsing GTFS-RT data, which is in Protobuf format.
- Evidence: `package.json` lists `protobufjs: ^7.4.0` as a dependency. `package-lock.json` shows `protobufjs` version `7.5.4`.
- Why it may be benign or suspicious: `protobufjs` is a legitimate library for handling Protocol Buffers. While a CVE (`CVE-2018-3738`) was found in older versions (up to 6.8.5), the skill uses version 7.5.4, which is not affected by this specific vulnerability.

## Suspicious Indicators (if any)
- Sensitive data access: The skill accesses `METRA_API_KEY` from environment variables. This is a legitimate and common practice for API authentication and is handled securely via HTTPS.
- Network endpoints: `gtfspublic.metrarr.com` and `schedules.metrarail.com`. Both are official Metra domains, making the network activity legitimate for the skill's purpose.
- Dangerous commands/APIs: The skill requires and uses the `unzip` system utility. This is explicitly documented as a requirement and is used for a specific, benign purpose (extracting official GTFS static data).

## Hidden or Undocumented Functionality
None detected. The `README.md` and `SKILL.md` files are exceptionally thorough, detailing all functionalities, data sources, requirements, and security/privacy considerations.

## Final Assessment
The skill is classified as **BENIGN**. The analysis reveals no credible evidence of malicious intent or high-risk behavior. All observed actions, including external API calls, data downloads, local file system writes, and environment variable access, are directly related to the skill's declared purpose of providing Metra transit information. The documentation is transparent and explicitly addresses security and privacy, stating that no user data is transmitted and no telemetry is collected. The dependencies are standard, and the `protobufjs` version used is not affected by known critical vulnerabilities.

## Recommended Action
ALLOW
The skill appears to be safe and performs its stated function without engaging in any malicious or high-risk activities.