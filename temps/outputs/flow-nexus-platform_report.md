# Agent Skill Security Analysis Report

## Overview
- Skill Name: flow-nexus-platform
- Declared Purpose: Comprehensive Flow Nexus platform management - authentication, sandboxes, app deployment, payments, and challenges
- Final Classification: BENIGN
- Overall Risk Level: HIGH
- Summary: This skill provides extensive capabilities for managing the Flow Nexus development platform. It includes user authentication, sandbox creation and arbitrary code execution, app deployment, payment management, coding challenges, file storage, and real-time features. While all functionalities align with the declared purpose of a development platform management tool, the ability to execute arbitrary code (`mcp__flow-nexus__sandbox_execute`), deploy applications with provided source code (`mcp__flow-nexus__app_store_publish_app`), and handle sensitive environment variables presents a significant attack surface. The skill itself is a powerful tool, not inherently malicious, but its capabilities carry a high risk of misuse or exploitation if an agent is compromised or instructed maliciously. External context regarding "mcp-remote" vulnerabilities underscores the potential for remote code execution in such client-server interactions.

## Observed Behaviors

### Behavior: User Authentication and Profile Management
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: Allows users to register, log in, manage passwords, verify emails, and update their profiles on the Flow Nexus platform.
- Evidence: `mcp__flow-nexus__user_register`, `mcp__flow-nexus__user_login`, `mcp__flow-nexus__user_reset_password`, `mcp__flow-nexus__user_profile`, etc.
- Why it may be benign or suspicious: Standard functionality for any platform requiring user accounts. Benign.

### Behavior: Sandbox Creation and Configuration
- Category: Legitimate Functionality, Privilege Abuse (potential)
- Technique ID (if applicable): PE1 — ExcessivePermissions (if sandbox configuration allows for overly broad permissions)
- Severity: MEDIUM
- Description: Enables the creation and configuration of isolated sandbox environments with specified templates, names, environment variables, package installations, and startup scripts.
- Evidence: `mcp__flow-nexus__sandbox_create({ template: "node", name: "my-sandbox", env_vars: { API_KEY: "your_api_key" }, install_packages: ["express"] })`, `mcp__flow-nexus__sandbox_configure`.
- Why it may be benign or suspicious: Benign for a development platform. Suspicious if `env_vars` or `startup_script` are used to inject malicious configurations or commands, or if the sandbox itself can be configured with excessive privileges.

### Behavior: Arbitrary Code Execution in Sandbox
- Category: Remote Execution
- Technique ID (if applicable): SC2 — RemoteScriptExecution
- Severity: HIGH
- Description: Allows the execution of arbitrary code (e.g., JavaScript, Python) within a designated sandbox environment. This is a core feature of a development platform.
- Evidence: `mcp__flow-nexus__sandbox_execute({ sandbox_id: "sandbox_id", code: \`console.log('Hello from sandbox!');\`, language: "javascript" })`
- Why it may be benign or suspicious: Benign as it's a fundamental capability for a development platform. Highly suspicious due to the inherent risk of arbitrary code execution. Even within a sandbox, vulnerabilities (sandbox escapes) could lead to broader system compromise. The web search context highlights RCE vulnerabilities in "mcp-remote" clients, which this skill effectively is, increasing the perceived risk.

### Behavior: File Upload to Sandbox and Storage
- Category: Data Exfiltration (potential), Remote Execution (potential)
- Technique ID (if applicable): P3 — ContextLeakageAndDataExfiltration (if used to exfiltrate data), SC2 — RemoteScriptExecution (if used to upload malicious scripts)
- Severity: MEDIUM
- Description: Provides functionality to upload files to specific sandboxes or general storage buckets (public, private, shared, temp).
- Evidence: `mcp__flow-nexus__sandbox_upload({ sandbox_id: "sandbox_id", file_path: "/app/config/database.json", content: JSON.stringify(databaseConfig) })`, `mcp__flow-nexus__storage_upload`.
- Why it may be benign or suspicious: Benign for managing project files and data. Suspicious if used to upload malicious payloads (e.g., scripts, executables) or to exfiltrate sensitive data from the agent's context or other accessible locations.

### Behavior: Application Publishing and Deployment
- Category: Remote Execution (indirect)
- Technique ID (if applicable): SC2 — RemoteScriptExecution
- Severity: MEDIUM
- Description: Enables publishing new applications or templates to an app store and deploying them, often by providing their source code and configuration variables.
- Evidence: `mcp__flow-nexus__app_store_publish_app({ name: "...", source_code: sourceCodeString, ... })`, `mcp__flow-nexus__template_deploy({ template_name: "...", variables: { api_key: "..." } })`
- Why it may be benign or suspicious: Benign for an app store and deployment platform. Suspicious if malicious source code is provided for deployment, potentially leading to persistent compromise or malicious services running on the platform.

### Behavior: Payment and Credit Management
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: Allows checking credit balances, viewing transaction history, purchasing credits via a payment link, and configuring auto-refill. Also includes programmatic earning of credits.
- Evidence: `mcp__flow-nexus__check_balance`, `mcp__flow-nexus__create_payment_link`, `mcp__flow-nexus__configure_auto_refill`, `mcp__flow-nexus__app_store_earn_ruv`.
- Why it may be benign or suspicious: Standard financial management for a paid service. Benign.

### Behavior: Coding Challenges and Gamification
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: Provides features to list, retrieve details, and submit solutions for coding challenges, as well as view leaderboards and achievements.
- Evidence: `mcp__flow-nexus__challenges_list`, `mcp__flow-nexus__challenge_submit`, `mcp__flow-nexus__leaderboard_get`.
- Why it may be benign or suspicious: Standard gamification features for a learning/development platform. Benign.

### Behavior: Real-time Subscriptions and Execution Monitoring
- Category: Legitimate Functionality
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: Allows subscribing to database changes and execution streams, and retrieving files generated during execution.
- Evidence: `mcp__flow-nexus__realtime_subscribe`, `mcp__flow-nexus__execution_stream_subscribe`, `mcp__flow-nexus__execution_file_get`.
- Why it may be benign or suspicious: Benign for monitoring and debugging within a development environment.

### Behavior: AI Assistant with Tool Usage
- Category: Agent Manipulation (potential), Remote Execution (indirect via AI)
- Technique ID (if applicable): P4 — BehaviorManipulation (if AI is manipulated), SC2 — RemoteScriptExecution (if AI uses tools to execute code)
- Severity: MEDIUM
- Description: Integrates an AI assistant (Queen Seraphina) that, when `enable_tools` is true, can utilize other skill capabilities (e.g., create swarms, deploy code).
- Evidence: `mcp__flow-nexus__seraphina_chat({ message: "...", enable_tools: true, ... })`
- Why it may be benign or suspicious: Benign for an AI-powered platform designed for automation. Suspicious because it delegates powerful, high-risk capabilities (like code execution and deployment) to an AI, which could be manipulated or misused to perform actions without direct human oversight for each step.

### Behavior: Handling of Sensitive Credentials
- Category: Credential Theft (potential)
- Technique ID (if applicable): E2 — CredentialHarvesting (if misused), PE3 — CredentialFileAccess (if accessing credential files within a sandbox)
- Severity: MEDIUM
- Description: The skill processes and uses sensitive credentials such as user passwords for authentication, and API keys, database URLs, and other secrets (e.g., `anthropic_key`, `NEXTAUTH_SECRET`) for configuring sandbox environments and deploying applications.
- Evidence: `mcp__flow-nexus__user_login({ email: "...", password: "..." })`, `env_vars: { API_KEY: "your_api_key", NODE_ENV: "development", DATABASE_URL: "postgres://..." }`, `anthropic_key: "sk-ant-..."`.
- Why it may be benign or suspicious: Benign as it's necessary for the platform's functionality (e.g., authenticating users, configuring secure environments). Suspicious if the agent is instructed to log, store insecurely, or exfiltrate these credentials, or if the skill itself has vulnerabilities in handling them.

## Suspicious Indicators
- Sensitive data access: The skill explicitly handles user passwords, API keys, database URLs, and other secrets (e.g., `anthropic_key`, `NEXTAUTH_SECRET`) as part of its legitimate configuration and authentication functions. While necessary, this makes it a target for credential harvesting if misused.
- Network endpoints: The skill interacts with the `flow-nexus.ruv.io` platform. Payment links are generated via `mcp__flow-nexus__create_payment_link` which returns a secure Stripe payment URL, indicating interaction with a third-party payment processor.
- Dangerous commands/APIs:
    - `mcp__flow-nexus__sandbox_execute`: Allows arbitrary code execution.
    - `mcp__flow-nexus__sandbox_upload`, `mcp__flow-nexus__storage_upload`: Allows uploading arbitrary files, which could include malicious scripts or exfiltrated data.
    - `mcp__flow-nexus__app_store_publish_app`, `mcp__flow-nexus__app_update`, `mcp__flow-nexus__template_deploy`: Allows deployment of arbitrary source code.
    - `mcp__flow-nexus__seraphina_chat` with `enable_tools: true`: Delegates powerful capabilities, including code execution and deployment, to an AI assistant.

## Hidden or Undocumented Functionality
None detected. All significant capabilities, including advanced configurations and the AI assistant's tool usage, are explicitly documented within the skill description.

## Final Assessment
The skill is classified as **BENIGN**. It is designed as a comprehensive management interface for a development platform, and its functionalities, including arbitrary code execution within sandboxes, application deployment, and file management, are core to its declared purpose. There is no direct evidence within the skill's code or metadata that indicates malicious intent or hidden harmful functionality.

However, the skill exposes a **HIGH** risk level due to the powerful and sensitive operations it can perform. The ability to execute arbitrary code (`sandbox_execute`) and deploy applications with user-provided source code (`app_store_publish_app`, `template_deploy`) means that if an agent using this skill were compromised or maliciously instructed, it could perform significant harmful actions, including remote code execution, data exfiltration via file uploads, or deployment of malicious services. The handling of sensitive credentials (API keys, database URLs, passwords) also presents a risk if not managed securely by the agent. The external context referencing "mcp-remote" vulnerabilities further highlights the inherent risks associated with such client-server interactions, even if the skill itself is not the source of a vulnerability.

## Recommended Action
REVIEW

The skill should be reviewed carefully before deployment. While benign, its powerful capabilities necessitate strict control over which agents can access it and how they are permitted to use its functions. Agents should be carefully audited to ensure they are not instructed to misuse the `sandbox_execute`, `sandbox_upload`, `app_store_publish_app`, or `template_deploy` functions for malicious purposes. Access to this skill should be granted only to trusted agents with a clear and legitimate need for its comprehensive platform management capabilities.