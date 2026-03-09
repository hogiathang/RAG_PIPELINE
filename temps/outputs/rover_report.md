# Agent Skill Security Analysis Report

## Overview
- Skill Name: charms
- Declared Purpose: Charms workflows for Bitcoin app contracts, spell proving, and UTXO asset operations.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The `charms` skill provides functionality for developing and operating programmable Bitcoin assets using the `charms` CLI tool, `bitcoin-cli`, and other standard Unix utilities. It requires high-privilege capabilities such as `process:spawn`, `http:outbound`, and `filesystem:read`, which are necessary for its stated purpose. While these capabilities carry inherent risks, the skill itself shows no direct evidence of malicious intent, credential theft, data exfiltration to unauthorized endpoints, or remote code execution of external payloads. It even includes explicit security warnings for users regarding sensitive data handling. The primary risk stems from the powerful `process:spawn` capability, which could be abused if user inputs are not properly sanitized by the orchestrating agent.

## Observed Behaviors

### Behavior: Execute external CLI commands
- Category: Remote Execution (local execution of pre-installed tools)
- Technique ID (if applicable): SC1 — CommandInjection (potential)
- Severity: MEDIUM
- Description: The skill explicitly requires and uses `bash`, `curl`, `jq`, `charms`, and `bitcoin-cli`. It leverages the `process:spawn` capability to execute these tools for tasks such as app scaffolding, building, spell validation, proving, wallet inspection, and Bitcoin network interactions. The `envsubst` utility is also used for environment variable substitution in spell files.
- Evidence: `metadata.oa.capabilities: - process:spawn`, "Requires `bash`, `curl`, and `jq`.", "Requires `charms` CLI.", "Requires `bitcoin-cli`", "Quick Commands" section showing `charms app new`, `charms spell check`, `charms wallet list`, `charms server`, `cd my-token`, `app_bin="$(charms app build)"`, `charms app vk "$app_bin"`, `cat ./spells/mint-nft.yaml | envsubst | charms spell check ...`.
- Why it may be benign or suspicious: Benign, as these are legitimate tools for the stated purpose of managing Bitcoin assets. Suspicious because `process:spawn` is a powerful capability that, if combined with unsanitized user input, could lead to command injection (SC1). The use of `envsubst` also introduces a vector for environment variable manipulation. However, the skill itself does not demonstrate malicious injection.

### Behavior: Read from the filesystem
- Category: FileSystemEnumeration
- Technique ID (if applicable): E3 — FileSystemEnumeration
- Severity: LOW
- Description: The skill declares `filesystem:read` capability and uses it to access local files such as spell definitions (`.yaml`), app binaries (`app_bin`), and prerequisite check scripts (`scripts/check-charms-prereqs.sh`).
- Evidence: `metadata.oa.capabilities: - filesystem:read`, `cat ./spells/mint-nft.yaml`, `app_bin="$(charms app build)"`, `charms app vk "$app_bin"`, `scripts/check-charms-prereqs.sh`.
- Why it may be benign or suspicious: Benign, as reading local files is essential for its function (e.g., loading spell definitions, app binaries, scripts). There is no evidence of attempting to read sensitive system files or credentials beyond what is necessary for its operation.

### Behavior: Make outbound HTTP requests and run an HTTP server
- Category: External Communication
- Technique ID (if applicable): E1 — ExternalTransmission
- Severity: MEDIUM
- Description: The skill declares `http:outbound` capability. It explicitly mentions running `charms server --ip 0.0.0.0 --port 17784` to expose an API endpoint for spell proving. It also requires `curl` for API interaction and `bitcoin-cli` which communicates with a Bitcoin node, implying outbound network requests.
- Evidence: `metadata.oa.capabilities: - http:outbound`, "Requires `curl`", "Run `charms server` and call `/spells/prove`", "Quick Commands: `charms server --ip 0.0.0.0 --port 17784`".
- Why it may be benign or suspicious: Benign, as network communication is necessary for interacting with Bitcoin nodes and for the `charms server` functionality. Suspicious because `http:outbound` can be used for data exfiltration or C2 communication. However, the skill's description clearly outlines the legitimate uses. The `charms server` binding to `0.0.0.0` makes it accessible externally if the host firewall allows, which is common for server applications but increases exposure.

### Behavior: Handle sensitive financial/cryptographic data with security warnings
- Category: Security Best Practices
- Technique ID (if applicable): P3 — ContextLeakageAndDataExfiltration (potential if not handled correctly by user)
- Severity: LOW
- Description: The skill interacts with Bitcoin UTXOs, funding addresses, and mentions "prover and wallet secrets." It explicitly advises users to "Keep prover and wallet secrets out of logs and source control" and to "Keep private inputs off-chain and pass them through the private input file path."
- Evidence: "Apply execution safety constraints: Keep prover and wallet secrets out of logs and source control.", "Keep private inputs off-chain and pass them through the private input file path.", `charms spell prove --funding-utxo="$funding_utxo" --funding-utxo-value="$funding_utxo_value" --change-address="$change_address"`.
- Why it may be benign or suspicious: Benign. The skill itself does not attempt to steal or exfiltrate these secrets. Instead, it provides explicit warnings and guidance on how users should handle them securely, indicating a responsible approach to sensitive data.

## Suspicious Indicators
- Sensitive data access: The skill interacts with Bitcoin wallet data and "prover and wallet secrets." However, it provides explicit warnings against exposing them, indicating a focus on user security rather than malicious intent. No direct evidence of the skill itself accessing or exfiltrating these.
- Network endpoints: The `charms server` command binds to `0.0.0.0:17784`. While a legitimate function, binding to all interfaces (`0.0.0.0`) exposes the service to the network, which could be a security concern depending on the environment and firewall rules.
- Dangerous commands/APIs: The `process:spawn` capability is inherently powerful and can be dangerous if not used carefully, especially when executing shell commands like `bash`, `curl`, `jq`, `envsubst`, and `bitcoin-cli`. These tools are legitimate for the skill's purpose but require careful handling of inputs to prevent command injection.

## Hidden or Undocumented Functionality
None detected. All capabilities and their uses appear to be openly declared and explained within the skill's description and examples. The `charms` project itself is open source and well-documented, further supporting transparency.

## Final Assessment
The skill is classified as **BENIGN**. The `charms` skill is designed to facilitate development and operations for programmable Bitcoin assets, a legitimate and well-defined purpose. It leverages standard, powerful command-line tools (`charms`, `bitcoin-cli`, `bash`, `curl`, `jq`, `envsubst`) and requires corresponding high-privilege capabilities (`process:spawn`, `http:outbound`, `filesystem:read`). While these capabilities, particularly `process:spawn`, introduce a potential for misuse (e.g., command injection if inputs are not sanitized), there is no direct evidence within the skill's code or description to suggest malicious intent, credential theft, unauthorized data exfiltration, or remote code execution of external payloads. The skill's explicit warnings about handling sensitive data responsibly further support its benign classification. The overall risk is rated MEDIUM due to the inherent power of the requested capabilities, which necessitate careful orchestration and input validation by the agent.

## Recommended Action
REVIEW
The skill should be reviewed. While classified as benign, its reliance on `process:spawn` and interaction with financial assets means that any input provided to the skill by the agent or user must be thoroughly sanitized to prevent command injection or other forms of abuse. The `charms server` binding to `0.0.0.0` also warrants review in a production environment to ensure appropriate network segmentation and firewall rules are in place.