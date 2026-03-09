# Agent Skill Security Analysis Report

## Overview
- Skill Name: Amadeus Hotels (with conflicting metadata for "expedia")
- Declared Purpose: Search hotel prices and availability via Amadeus API.
- Final Classification: MALICIOUS
- Overall Risk Level: MEDIUM
- Summary: The primary functionality described for the "Amadeus Hotels" skill appears benign, focusing on legitimate API interactions for hotel search and tracking. However, the presence of a `metadata.json` file describing a *different* skill ("expedia") from a *different* repository, coupled with a `downloaded_at` timestamp set in the future (2026), indicates a severe package integrity issue. This conflicting and manipulated metadata suggests an attempt to obscure the true nature or origin of the package, making it suspicious and potentially malicious.

## Observed Behaviors

### Behavior: External API Communication
- Category: Legitimate Functionality
- Technique ID (if applicable): E1 — ExternalTransmission (benign use)
- Severity: LOW
- Description: The skill is designed to communicate with the Amadeus Self-Service API to retrieve hotel information.
- Evidence: `developers.amadeus.com` is mentioned as the API endpoint throughout `README.md` and `SKILL.md`. The skill requires `AMADEUS_API_KEY` and `AMADEUS_API_SECRET` for authentication.
- Why it may be benign or suspicious: This is the core, declared purpose of the skill and is benign. API keys are handled via environment variables, which is a standard security practice.

### Behavior: External Command Execution
- Category: Legitimate Functionality
- Technique ID (if applicable): SC1 — CommandInjection (potential, but declared)
- Severity: LOW
- Description: The skill explicitly requires and executes `python3` scripts and uses `pip install` for dependencies.
- Evidence: `SKILL.md` lists `python3` under `bins` requirement and `pip` for `requests` package installation. Usage examples show `python3 scripts/search.py`, `python3 scripts/offers.py`, etc.
- Why it may be benign or suspicious: For a Python-based skill, executing `python3` and `pip` is expected and necessary. While external command execution always carries inherent risk if the executed code is malicious, the *declared* purpose here is benign.

### Behavior: Credential Handling
- Category: Legitimate Functionality
- Technique ID (if applicable): None (secure handling)
- Severity: LOW
- Description: The skill requires API credentials (key and secret) to be set as environment variables.
- Evidence: `README.md` and `SKILL.md` instruct users to `export AMADEUS_API_KEY="your-api-key"` and `export AMADEUS_API_SECRET="your-api-secret"`.
- Why it may be benign or suspicious: Using environment variables is a secure way to manage API credentials, preventing them from being hardcoded in the skill's scripts. This is a benign practice.

### Behavior: Package Metadata Manipulation / Inconsistency
- Category: Agent Manipulation / Hidden Functionality
- Technique ID (if applicable): P4 — BehaviorManipulation, SC3 — ObfuscatedCode
- Severity: HIGH
- Description: The package contains a `metadata.json` file that describes a completely different skill ("expedia") from a different GitHub repository (`Andrejones92/canifi-life-os`) and has a `downloaded_at` timestamp set to a future date (2026-01-22). This directly conflicts with the `_meta.json` and `README.md` files which describe the "Amadeus Hotels" skill.
- Evidence:
    - `_meta.json`: `"slug": "amadeus-hotels"`, `"owner": "kesslerio"`, `"commit": "https://github.com/clawdbot/skills/commit/b386452faa36fb46ffb7e6af77fff094ecc46264"`
    - `metadata.json`: `"name": "expedia"`, `"repo": "Andrejones92/canifi-life-os"`, `"downloaded_at": "2026-01-22T01:42:24.952290Z"`
- Why it may be benign or suspicious: This is highly suspicious. The presence of conflicting metadata for a different skill, especially with a future timestamp, strongly suggests an attempt to manipulate the agent's understanding of the package, its origin, or its download time. This could be an attempt to bypass security checks, obscure the true nature of the package, or indicate a tampered package. It undermines the integrity and trustworthiness of the skill package.

## Suspicious Indicators
- Sensitive data access: None directly observed in the *Amadeus Hotels* skill's *intended* functionality beyond requiring API keys via environment variables (which is standard).
- Network endpoints: `developers.amadeus.com` (legitimate for the skill's purpose).
- Dangerous commands/APIs: `python3` and `pip install` are used, which are powerful but declared and necessary for the skill's operation. The danger lies in the *content* of the Python scripts, which are not provided for analysis.

## Hidden or Undocumented Functionality
The primary hidden functionality is the presence of the `metadata.json` file describing a completely different skill ("expedia") with a future `downloaded_at` timestamp. This metadata is not declared or explained in the `README.md` or `SKILL.md` for the "Amadeus Hotels" skill and directly contradicts its identity. This constitutes a significant integrity issue for the package.

## Final Assessment
The skill is classified as **MALICIOUS** not because of the *declared functionality* of the "Amadeus Hotels" skill, which appears benign, but due to the severe **package integrity issues** identified. The `metadata.json` file, which describes a different skill ("expedia") from a different repository and contains a `downloaded_at` timestamp set in the future, is a strong indicator of manipulation or an attempt to obscure the package's true nature or origin. This kind of metadata inconsistency and temporal anomaly is a high-risk behavior that compromises the trustworthiness of the entire skill package. It suggests an intent to deceive or bypass standard verification processes.

## Recommended Action
BLOCK
The package should be blocked due to the critical integrity issues and suspicious metadata manipulation. While the "Amadeus Hotels" functionality itself seems benign, the presence of conflicting and manipulated metadata for a different skill within the same package is a significant security risk that cannot be overlooked. It indicates a potentially tampered or maliciously constructed package.