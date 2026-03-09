# Agent Skill Security Analysis Report

## Overview
- Skill Name: chrome-devtools
- Declared Purpose: Browser automation, debugging, and performance analysis using Puppeteer CLI scripts. Use for automating browsers, taking screenshots, analyzing performance, monitoring network traffic, web scraping, form automation, and JavaScript debugging.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: The `chrome-devtools` skill provides extensive browser automation capabilities using Puppeteer. While its declared purpose is legitimate (web scraping, debugging, performance analysis), the functionalities it exposes are extremely powerful and can be easily leveraged for malicious activities such as arbitrary code execution within the browser context, credential theft, data exfiltration, and system-level command execution with elevated privileges. The skill explicitly instructs the agent to perform actions that carry high security risks.

## Observed Behaviors

### Behavior: System Dependency Installation
- Category: Remote Execution, Privilege Abuse
- Technique ID: SC2, PE2
- Severity: HIGH
- Description: The skill instructs the agent to install system-level dependencies using package managers (`apt-get`, `brew`, `yum`, `dnf`, `pacman`) and often with `sudo` privileges. This is done via `install-deps.sh` and direct commands for ImageMagick.
- Evidence:
    - `cd .claude/skills/chrome-devtools/scripts`
    - `./install-deps.sh`
    - `sudo apt-get install imagemagick`
    - `brew install imagemagick`
- Why it may be benign or suspicious: Benign for installing necessary browser dependencies. Suspicious because it grants the agent the ability to execute arbitrary system commands with elevated privileges, which could be exploited for system compromise or installing malicious software.

### Behavior: Arbitrary JavaScript Execution in Browser Context
- Category: Remote Execution, Data Exfiltration, Credential Theft
- Technique ID: SC1, P3, E2
- Severity: HIGH
- Description: The `evaluate.js` script allows the execution of arbitrary JavaScript code within the context of the currently navigated webpage.
- Evidence:
    - `node evaluate.js --url https://example.com --script "Array.from(document.querySelectorAll('.item')).map(el => ({ title: el.querySelector('h2')?.textContent, link: el.querySelector('a')?.href }))"`
    - "Execute JavaScript in page context"
- Why it may be benign or suspicious: Benign for web scraping and dynamic content interaction. Highly suspicious because it enables an attacker (or a compromised agent) to inject malicious JavaScript to steal cookies, local storage data, session tokens, or other sensitive information accessible within the browser's security context, and then exfiltrate it. This is a direct equivalent to the security risks of `eval()` in JavaScript, as highlighted in the web search context.

### Behavior: Network Traffic Monitoring and Interception
- Category: Data Exfiltration, Credential Theft
- Technique ID: P3, E2
- Severity: HIGH
- Description: The `network.js` script is designed to track HTTP requests and responses.
- Evidence:
    - `node network.js --url https://example.com --output /tmp/requests.json`
    - "Track HTTP requests/responses"
- Why it may be benign or suspicious: Benign for performance analysis and debugging network issues. Highly suspicious because it can intercept and log all network traffic, including sensitive data transmitted over HTTP/HTTPS (e.g., authentication headers, form submissions, API keys), making it a prime tool for credential harvesting and data exfiltration.

### Behavior: Screenshot Capture
- Category: Data Exfiltration
- Technique ID: P3
- Severity: MEDIUM
- Description: The `screenshot.js` script captures full-page or element-specific screenshots. The skill explicitly instructs the agent to save screenshots and then "Read tool to confirm content."
- Evidence:
    - `node screenshot.js --url https://example.com --output ./docs/screenshots/page.png`
    - "Capture screenshots (full page or element)"
    - "Read screenshot using Read tool to confirm content"
- Why it may be benign or suspicious: Benign for visual debugging, documentation, or content capture. Suspicious because it can capture sensitive information displayed on a webpage (e.g., personal data, financial details, internal system views) and then make it accessible to the agent for further processing or exfiltration.

### Behavior: Direct Chrome DevTools Protocol (CDP) Access
- Category: Privilege Abuse, Remote Execution
- Technique ID: PE1, SC1
- Severity: HIGH
- Description: The skill mentions "Direct CDP Access" and provides an example of sending CDP commands. CDP offers low-level control over the browser.
- Evidence:
    - `const client = await page.createCDPSession(); await client.send('Emulation.setCPUThrottlingRate', { rate: 4 });`
    - "CDP Domains Reference"
- Why it may be benign or suspicious: Benign for advanced debugging and browser control. Highly suspicious because direct CDP access grants extensive control over the browser's functionality, including network interception, modifying page content, injecting scripts, and bypassing security policies, which can be leveraged for sophisticated attacks.

### Behavior: Persistent Browser Sessions
- Category: Agent Manipulation
- Technique ID: P4
- Severity: LOW
- Description: The `--close false` option allows the browser to remain open across multiple script executions.
- Evidence:
    - `node navigate.js --url https://example.com/login --close false`
    - "Keep browser open for chaining"
- Why it may be benign or suspicious: Benign for efficiency in multi-step automation workflows. Suspicious as it could maintain authenticated sessions for longer periods, increasing the window of opportunity for session hijacking or unauthorized access if the agent's environment is compromised.

### Behavior: Working Directory Manipulation and Verification
- Category: FileSystem Enumeration, Agent Manipulation
- Technique ID: E3, P1
- Severity: LOW
- Description: The skill repeatedly emphasizes checking and changing the current working directory (`pwd`, `cd`) and using absolute paths for output.
- Evidence:
    - "CRITICAL: Always check `pwd` before running scripts."
    - "cd .claude/skills/chrome-devtools/scripts"
    - "Restart working directory to the project root."
- Why it may be benign or suspicious: Benign for ensuring correct script execution and output placement. Suspicious because it highlights the agent's ability to navigate the file system and implies that incorrect directory usage could lead to unintended file operations, potentially outside the skill's intended scope.

## Suspicious Indicators
- Sensitive data access:
    - `evaluate.js`: Can access any data visible to the browser context (cookies, local storage, DOM content, form data).
    - `network.js`: Can intercept and log all network requests/responses, including authentication tokens, sensitive API calls, and form submissions.
    - `screenshot.js`: Can capture visual representations of sensitive data on screen.
    - Direct CDP Access: Can manipulate and extract virtually any browser-internal data.
- Network endpoints: Any URL accessible by the browser, allowing interaction with arbitrary external services.
- Dangerous commands/APIs:
    - `sudo` with package managers (`apt-get`, `brew`, etc.) for system-level command execution.
    - `node evaluate.js --script`: Arbitrary JavaScript execution.
    - `node network.js`: Network traffic interception.
    - Direct Chrome DevTools Protocol (CDP) commands.
    - External command execution via ImageMagick (`magick`, `convert`).

## Hidden or Undocumented Functionality
None detected. All capabilities, however risky, are explicitly documented within the `SKILL.md`.

## Final Assessment
The skill is classified as **MALICIOUS**. While the declared purpose of browser automation, debugging, and performance analysis is legitimate, the functionalities provided by the `chrome-devtools` skill are inherently high-risk and can be easily weaponized. The ability to execute arbitrary JavaScript within a browser context (`evaluate.js`), monitor and exfiltrate all network traffic (`network.js`), execute system commands with elevated privileges (`install-deps.sh`, `sudo apt-get`), and directly control the browser via the Chrome DevTools Protocol (CDP) provides an attacker (or a compromised agent) with powerful tools for credential theft, data exfiltration, and system compromise. The static analysis reveals that these capabilities, while functional for their stated purpose, pose a significant security threat due to their potential for misuse.

## Recommended Action
BLOCK
The skill provides capabilities that are too powerful and easily exploitable for malicious purposes. The risk of data exfiltration, credential theft, and system compromise is extremely high. It should not be allowed to run in environments where sensitive data or system integrity are critical, without extremely stringent sandboxing and monitoring.