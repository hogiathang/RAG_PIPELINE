# Agent Skill Security Analysis Report

## Overview
- Skill Name: video-skill
- Declared Purpose: Run the video-skill pipeline to convert narrated videos into structured step data and enriched timeline-ready outputs. It processes videos into steps, performs transcription, chunking, extraction, enrichment, and generates markdown from extracted skills. It also supports debugging provider connectivity.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: The `video-skill` agent skill is designed to process video content using AI models and media tools like `ffmpeg`. All observed behaviors, including local command execution (`uv`, `ffmpeg`, `docker`) and interaction with AI model endpoints, are consistent with its declared purpose. The skill is configured to use self-hosted or local AI services, and API keys are expected to be managed via environment variables, indicating a focus on controlled and secure operation. No evidence of malicious intent, unauthorized data exfiltration, or credential theft was found.

## Observed Behaviors

### Behavior: Local Command Execution
- Category: Legitimate Functionality
- Technique ID (if applicable): SC2 (but benign use)
- Severity: LOW
- Description: The skill executes local binaries such as `uv` (a Python package manager/runner), `ffmpeg` (a multimedia framework), and `docker compose` (for managing local containerized services). These commands are used to install dependencies, run the Python application, process video files, and set up local AI model services.
- Evidence:
    - `SKILL.md`: `metadata: { "openclaw": { "requires": { "bins": ["uv", "ffmpeg", "python3"] } } }`
    - `README.md`: `uv sync --dev`, `uv run ruff check .`, `uv run pytest -q`, `./scripts/bootstrap_models.sh`, `docker compose -f deploy/docker-compose.models.yml up -d`, `uv run video-skill <command>`.
- Why it may be benign or suspicious: This is a benign behavior. The binaries are explicitly declared requirements and are standard tools for the skill's stated purpose (video processing, AI model interaction, Python application execution). The commands are well-defined and do not indicate an attempt to execute arbitrary or malicious remote code.

### Behavior: Configuration for AI Model Interaction
- Category: Legitimate Functionality
- Technique ID (if applicable): None
- Severity: LOW
- Description: The skill uses a `config.json` file (based on `config.example.json`) to define endpoints for transcription, reasoning, and vision-language models (VLM). These endpoints are explicitly set to `http://YOUR_SERVER_IP:PORT`, indicating an intention to use local or self-hosted AI services.
- Evidence:
    - `config.example.json`:
        ```json
        {
          "transcription": { "provider": "whisper-local", "base_url": "http://YOUR_SERVER_IP:8003", ... },
          "reasoning": { "provider": "openai-compatible", "base_url": "http://YOUR_SERVER_IP:8001", ... },
          "vlm": { "provider": "openai-compatible", "base_url": "http://YOUR_SERVER_IP:8002", ... }
        }
        ```
    - `README.md`: "Model setup (local/self-hosted)", "Start model stack `docker compose -f deploy/docker-compose.models.yml up -d`".
- Why it may be benign or suspicious: This is a benign behavior. The configuration clearly points to local/self-hosted services, which is a secure approach for AI model interaction. It does not indicate an attempt to exfiltrate data to unknown external parties.

### Behavior: API Key Handling via Environment Variables
- Category: Legitimate Functionality / Secure Practice
- Technique ID (if applicable): None
- Severity: LOW
- Description: The configuration suggests that API keys for AI model providers should be handled via environment variables (`api_key_env: null` in `config.example.json`), rather than being hardcoded or transmitted insecurely.
- Evidence:
    - `config.example.json`: `"api_key_env": null` for all provider configurations.
- Why it may be benign or suspicious: This is a benign and recommended security practice. It prevents sensitive credentials from being exposed in configuration files or source code. There is no evidence of credential harvesting.

### Behavior: File System Access (Read/Write)
- Category: Legitimate Functionality
- Technique ID (if applicable): E3 — FileSystemEnumeration (but benign use)
- Severity: LOW
- Description: The skill reads video files as input and writes various intermediate and final output files (e.g., `*.whisper.json`, `*.segments.jsonl`, `*.steps.ai.jsonl`, `*.md`, image frames to directories). This is necessary for its video processing and data transformation purpose.
- Evidence:
    - `README.md` and `SKILL.md` demonstrate commands like:
        - `video-skill transcribe --video datasets/demo/zac-game.mp4 --out datasets/demo/zac-game.whisper.json`
        - `video-skill frames-extract --video <video.mp4> --out-dir datasets/demo/frames_zac_game`
        - `video-skill markdown-render --out datasets/demo/zac-game.md`
- Why it may be benign or suspicious: This is a benign behavior. The file system operations are directly related to the skill's core functionality of processing input videos and generating structured output data. There is no indication of unauthorized or excessive file system access.

## Suspicious Indicators (if any)
- Sensitive data access: None detected. API keys are expected via environment variables, not accessed directly by the skill in a suspicious manner.
- Network endpoints: The skill is configured to interact with `http://YOUR_SERVER_IP:PORT` for AI models, explicitly for local/self-hosted services. No external, arbitrary, or undeclared network endpoints are targeted.
- Dangerous commands/APIs: The commands `uv`, `ffmpeg`, `docker compose` are standard tools used for their legitimate purposes within the skill's scope. No inherently dangerous or misused commands were identified.

## Hidden or Undocumented Functionality
None detected. The `SKILL.md` description, `README.md`, and other documentation clearly explain the skill's purpose and capabilities, which are consistent with the observed code and configuration.

## Final Assessment
The `video-skill` is classified as **BENIGN**. The static analysis of all provided files (`INSTRUCTIONS.md`, `_meta.json`, `config.example.json`, `IMPLEMENTATION_REFS.md`, `README.md`, `SKILL.md`, `BACKLOG.md`, `v2-research.md`) reveals a well-documented and purposeful application. All observed behaviors, including local command execution, file system access, and AI model interaction, are directly aligned with the skill's declared goal of processing videos into structured steps. The configuration explicitly points to local/self-hosted AI services, and API key handling is designed to be secure via environment variables. There is no evidence of malicious intent, credential theft, unauthorized data exfiltration, privilege abuse, or hidden functionality.

## Recommended Action
ALLOW
The skill appears to be safe and serves a legitimate purpose. It adheres to good security practices for API key management and local service interaction.