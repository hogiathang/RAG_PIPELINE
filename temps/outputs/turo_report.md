# Agent Skill Security Analysis Report

## Overview
- Skill Name: pptx (as described in SKILL.md, metadata.json uses "turo")
- Declared Purpose: Presentation creation, editing, and analysis. Working with .pptx files for creation, modification, layout, comments, and speaker notes.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The skill provides comprehensive instructions and workflows for creating, editing, and analyzing PowerPoint (.pptx) files using a combination of Python scripts, command-line tools (LibreOffice, Poppler), and JavaScript libraries (PptxGenJS, Playwright, Sharp). Its functionality is entirely aligned with its declared purpose of document processing. The primary risks stem from the use of external dependencies, some of which have known vulnerabilities (e.g., PptxGenJS XSS) or are general vectors for supply chain attacks (npm packages). The skill itself does not exhibit malicious behavior, but the environment in which it operates and the handling of untrusted input through its tools could introduce risks.

## Observed Behaviors

### Behavior: File System Access (Read/Write)
- Category: Legitimate Functionality
- Technique ID (if applicable): E3 — FileSystemEnumeration
- Severity: LOW
- Description: The skill extensively reads and writes various file types, including `.pptx`, `.xml`, `.json`, `.md`, `.html`, `.pdf`, `.jpg`, and `.png`. This is fundamental to its purpose of processing and manipulating presentation files.
- Evidence:
    - `python -m markitdown path-to-file.pptx` (reads .pptx, writes .md)
    - `python ooxml/scripts/unpack.py <office_file> <output_dir>` (reads .pptx, writes .xml files)
    - `python ooxml/scripts/pack.py <input_directory> <office_file>` (reads .xml files, writes .pptx)
    - `python scripts/inventory.py working.pptx text-inventory.json` (reads .pptx, writes .json)
    - `python scripts/replace.py working.pptx replacement-text.json output.pptx` (reads .pptx, .json, writes .pptx)
    - `python scripts/thumbnail.py template.pptx [output_prefix]` (reads .pptx, writes .jpg)
    - `soffice --headless --convert-to pdf template.pptx` (reads .pptx, writes .pdf)
    - `pdftoppm -jpeg -r 150 template.pdf slide` (reads .pdf, writes .jpg)
    - `sharp(...).toFile(filename)` (writes .png for icons/gradients)
    - `pptx.writeFile('output.pptx')` (writes .pptx)
- Why it may be benign or suspicious: This is a core, benign behavior for a document processing skill.

### Behavior: External Command Execution
- Category: Legitimate Functionality
- Technique ID (if applicable): SC1 — CommandInjection (potential, but not directly observed as malicious)
- Severity: MEDIUM
- Description: The skill instructs the agent to execute various command-line tools and Python scripts for document conversion, manipulation, and analysis.
- Evidence:
    - `python -m markitdown`
    - `python ooxml/scripts/unpack.py`
    - `python ooxml/scripts/validate.py`
    - `python ooxml/scripts/pack.py`
    - `python scripts/rearrange.py`
    - `python scripts/inventory.py`
    - `python scripts/replace.py`
    - `python scripts/thumbnail.py`
    - `soffice --headless --convert-to pdf`
    - `pdftoppm -jpeg`
    - `npm install -g pptxgenjs`, `npm install -g playwright`, `npm install -g react-icons`, `npm install -g sharp` (dependency installation commands)
    - `sudo apt-get install libreoffice`, `sudo apt-get install poppler-utils` (dependency installation commands)
- Why it may be benign or suspicious: The commands are standard tools for document processing and are directly relevant to the skill's purpose. The Python scripts are local to the skill. The `npm install -g` and `sudo apt-get install` commands are for dependency setup, not runtime execution by the skill itself, but they highlight the need for a secure environment. The risk is elevated to MEDIUM due to the potential for command injection if user input is not properly sanitized when passed to these commands, though the skill itself doesn't demonstrate this.

### Behavior: Use of Headless Browser (Playwright)
- Category: Legitimate Functionality
- Severity: LOW
- Description: The skill uses Playwright for rendering HTML slides to facilitate conversion to PowerPoint.
- Evidence: `html2pptx.md` and `SKILL.md` mention `playwright` as a dependency and for HTML rendering.
- Why it may be benign or suspicious: Playwright is a powerful tool capable of network requests. However, its described use within this skill is for local HTML rendering and rasterization, which is a legitimate use case. There's no instruction to navigate to arbitrary external URLs.

### Behavior: Dependency on External Libraries with Known Vulnerabilities
- Category: Dependency Risk
- Technique ID (if applicable): SC2 — RemoteScriptExecution (indirectly, via supply chain)
- Severity: MEDIUM
- Description: The skill relies on `pptxgenjs`, which has a reported XSS vulnerability (GitHub Issue #350). Additionally, the use of `npm` packages in general introduces a supply chain risk, as highlighted by the web search context regarding npm supply chain attacks.
- Evidence:
    - `pptxgenjs` is listed as a dependency and extensively used in `html2pptx.md`.
    - Web search context: "XSS (High Level Vulnerability Security Warning) · Issue #350 - GitHub" for `PptxGenJS`.
    - Web search context: "npm Supply Chain Attack via Open Source maintainer compromise" for general npm risk.
- Why it may be benign or suspicious: While the skill itself doesn't exploit these vulnerabilities, its reliance on a dependency with a known XSS issue means that if the skill processes untrusted input (e.g., user-provided HTML or text) and feeds it directly into `PptxGenJS` without proper sanitization, it could become a vector for exploitation. The general npm supply chain risk is inherent to using npm packages.

### Behavior: Secure XML Parsing
- Category: Security Best Practice
- Severity: LOW
- Description: The skill explicitly lists `defusedxml` as a dependency, which is used for secure XML parsing.
- Evidence: `defusedxml`: `pip install defusedxml` (for secure XML parsing)
- Why it may be benign or suspicious: This is a positive security indicator, showing awareness of XML parsing vulnerabilities and taking steps to mitigate them.

## Suspicious Indicators
- Sensitive data access: None detected. The skill focuses on document content.
- Network endpoints: No direct network endpoints are accessed by the skill's instructions for data exfiltration. Playwright is used for local rendering, not external browsing.
- Dangerous commands/APIs: The use of `soffice` (LibreOffice) and `pdftoppm` (Poppler) are powerful system tools. While used for legitimate document conversion here, their broad capabilities could be misused if the skill were modified or given malicious input. The `npm install -g` and `sudo apt-get install` commands, if executed at runtime by the agent, represent privilege abuse, but are presented as dependency setup instructions.

## Hidden or Undocumented Functionality
None detected. The skill's documentation (`SKILL.md`, `ooxml.md`, `html2pptx.md`) is very detailed and transparent about its capabilities and workflows.

## Final Assessment
The skill is classified as **BENIGN**. Its entire functionality is dedicated to the legitimate purpose of creating, editing, and analyzing PowerPoint presentations. The instructions are clear, and the tools used are appropriate for the task. There is no direct evidence of malicious intent, credential theft, data exfiltration, or unauthorized remote execution within the provided code and documentation.

However, the skill's reliance on external dependencies, particularly `PptxGenJS` which has a reported XSS vulnerability, and the general risks associated with the `npm` ecosystem (supply chain attacks), elevate the overall risk level to **MEDIUM**. If the agent were to process untrusted user-provided content (e.g., HTML, text for charts/tables) through this skill without robust input sanitization, these dependency vulnerabilities could potentially be exploited. The use of powerful system tools like LibreOffice and Poppler also warrants careful handling of input to prevent potential abuse, though the skill itself does not demonstrate such abuse.

## Recommended Action
REVIEW
The skill is benign in its intent and functionality. However, due to the identified dependency risks (PptxGenJS XSS, general npm supply chain), it should be reviewed to ensure that:
1. The agent environment securely manages and scans dependencies for vulnerabilities.
2. Any user-provided input processed by this skill (especially HTML or text that will be rendered by PptxGenJS) is thoroughly sanitized to prevent XSS or other injection attacks.
3. The execution environment for `soffice` and `pdftoppm` is sandboxed if processing untrusted files.