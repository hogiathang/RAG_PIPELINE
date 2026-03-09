# Agent Skill Security Analysis Report

## Overview
- Skill Name: A-Corp Foundry
- Declared Purpose: A-Corp Foundry — the coordination engine for agentic companies. Register, learn the system, and discover specialized skills.
- Final Classification: BENIGN
- Overall Risk Level: MEDIUM
- Summary: The A-Corp Foundry skill provides comprehensive API documentation for managing decentralized autonomous organizations (A-Corps). It outlines functionalities for participants (creating A-Corps, voting, trading, preparing execution intents), and operators (KYC, claiming A-Corps, managing compliance, and exercising critical safety controls like freezing participants/outflows, and even killing an A-Corp). While the skill exposes highly privileged and financially impactful operations, these are explicitly documented as part of the platform's intended design for managing complex, on-chain entities. The documentation includes clear role-based access controls and behavioral rules. The risk is primarily associated with the potential misuse of these powerful, but legitimate, capabilities by a compromised or malicious actor, rather than the skill itself being inherently malicious.

## Observed Behaviors

### Behavior: API Key Handling
- Category: Authentication
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill requires an API key for most authenticated requests, issued upon registration. It explicitly warns users to save their API key as it cannot be retrieved later and to never send it to any domain other than `api.acorpfoundry.ai`.
- Evidence:
    - `Authorization: Bearer <your_acorp_api_key>`
    - `POST /participants/register` response: `"important": "Save your api_key — it cannot be retrieved later."`
    - `SKILL.md`: "**CRITICAL:** Never send your A-Corp Foundry API key to any domain other than `api.acorpfoundry.ai`."
- Why it may be benign or suspicious: This is standard and secure API key management practice, including explicit warnings against credential leakage. Benign.

### Behavior: Financial Transactions (Contributions & Withdrawals)
- Category: Financial Operations
- Technique ID (if applicable): N/A
- Severity: MEDIUM
- Description: The skill allows participants to contribute USDC to an A-Corp's treasury and record withdrawals. Operators can configure velocity limits and freeze/unfreeze treasury outflows.
- Evidence:
    - `POST https://api.acorpfoundry.ai/treasury/<acorpId>/treasury/contribute`
    - `POST https://api.acorpfoundry.ai/velocity/<acorpId>/record`
    - `POST https://api.acorpfoundry.ai/velocity/<acorpId>/freeze`
- Why it may be benign or suspicious: These are core functionalities for managing an on-chain treasury. While legitimate, unauthorized use of these endpoints (e.g., by a compromised agent) could lead to financial loss or manipulation. The skill notes that `contribute` returns wallet instructions, implying off-chain user confirmation. Benign, but high impact if misused.

### Behavior: Smart Contract Interaction & Execution
- Category: On-chain Operations
- Technique ID (if applicable): N/A
- Severity: HIGH
- Description: The skill allows preparing execution intents for on-chain actions, including `deploy_contract`. Proposals can also include `treasuryTransfers` and `executionTarget`/`executionData` for smart contract calls.
- Evidence:
    - `POST https://api.acorpfoundry.ai/execution/prepare` with `payload: {"action": "deploy_contract", ...}`
    - `POST https://api.acorpfoundry.ai/execution/<intentId>/submit`
    - `POST https://api.acorpfoundry.ai/proposals/<acorpId>/create` with `"treasuryTransfers": [...]` and `"executionTarget" / "executionData"`
- Why it may be benign or suspicious: These are powerful capabilities for a DAO, enabling direct interaction with smart contracts and on-chain assets. The skill explicitly states that `execution/prepare` is "Blocked if: A-Corp is not `active`/`executing`, delegation expired, risk tolerance exceeded, or risk score above escalation threshold," indicating built-in safety mechanisms. However, if these safeguards are bypassed or misconfigured, deploying malicious contracts or executing unauthorized transfers poses a significant risk. Benign, but extremely high impact if misused.

### Behavior: Designated Decision Maker (DDM) Actions
- Category: Privilege Abuse / Financial Operations
- Technique ID (if applicable): PE1
- Severity: MEDIUM
- Description: A DDM can be nominated and, once elected, can `act` on behalf of the A-Corp, including performing `treasury_transfer` actions within defined constraints.
- Evidence:
    - `POST https://api.acorpfoundry.ai/decision-maker/<acorpId>/act` with `{"actionType": "treasury_transfer", ...}`
- Why it may be benign or suspicious: This is a legitimate governance mechanism for day-to-day decisions. The constraints are designed to limit risk. However, if a DDM's API key is compromised or if the constraints are set too broadly, it could lead to unauthorized financial transfers. Benign, but high impact if misused.

### Behavior: Operator Kill Switch
- Category: Destructive Actions / Privilege Abuse
- Technique ID (if applicable): PE1
- Severity: HIGH
- Description: Operators have the authority to "kill" an A-Corp, which permanently dissolves it and donates treasury funds to the AI Displacement Fund. This action is explicitly stated as "irreversible."
- Evidence:
    - `POST https://api.acorpfoundry.ai/operator/acorp/<acorpId>/kill`
    - `operator-agent.md`: "Permanently dissolves the A-Corp. Treasury funds are donated to the AI Displacement Fund. This is irreversible."
- Why it may be benign or suspicious: This is a critical, high-impact safety mechanism for legal oversight by human operators. While intended for extreme situations, if an operator's API key is compromised, it could be used maliciously to destroy an A-Corp and its assets. Benign, but represents the highest level of destructive capability.

### Behavior: Operator Graduated Response Controls
- Category: Privilege Abuse / Agent Manipulation
- Technique ID (if applicable): PE1, P4
- Severity: HIGH
- Description: Operators can pause/unpause an A-Corp, freeze/unfreeze individual participants, and freeze/unfreeze treasury outflows.
- Evidence:
    - `POST https://api.acorpfoundry.ai/operator/acorp/<acorpId>/pause`
    - `POST https://api.acorpfoundry.ai/operator/acorp/<acorpId>/freeze-participant`
    - `POST https://api.acorpfoundry.ai/operator/acorp/<acorpId>/freeze-outflows`
- Why it may be benign or suspicious: These are essential safety and regulatory controls for operators to manage risk and respond to incidents. If an operator's API key is compromised, these controls could be abused to disrupt A-Corp operations or unfairly target participants. Benign, but high impact if misused.

### Behavior: Role-Based Access Control
- Category: Privilege Management
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill clearly defines different roles (participant, operator, admin) and restricts certain high-impact actions to specific roles or the A-Corp creator.
- Evidence:
    - "Creator Only" for `PATCH /treasury/<acorpId>/treasury/access`
    - "Operator Only" for `POST /velocity/<acorpId>/config`
    - "Admin Only" for `POST /revenue/record`
    - Operator routes require `<operator_api_key>`
- Why it may be benign or suspicious: This is a fundamental security principle for managing access to sensitive functions. Benign.

### Behavior: Delegation Constraints
- Category: Agent Safety / Self-Imposed Limits
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: Participants can set self-imposed operating boundaries (budget caps, risk tolerance, red lines, expiry) that are enforced by the platform before signals and execution intents.
- Evidence:
    - `POST https://api.acorpfoundry.ai/participant/delegation`
    - `acorp-participant.md`: "Blocked if: A-Corp is not `active`/`executing`, delegation expired, risk tolerance exceeded, or risk score above escalation threshold."
- Why it may be benign or suspicious: This is a proactive safety feature designed to prevent an agent from exceeding its defined boundaries. Benign.

## Suspicious Indicators
- Sensitive data access: The skill handles API keys, wallet addresses, and financial transaction details (USDC amounts, ERC20 token addresses). This is inherent to its purpose.
- Network endpoints: All interactions are via HTTPS to `https://api.acorpfoundry.ai`. No external, unknown endpoints are indicated.
- Dangerous commands/APIs:
    - `operator/acorp/<acorpId>/kill`: Irreversible A-Corp dissolution and fund donation.
    - `execution/prepare` with `deploy_contract`: Potential for deploying malicious smart contracts.
    - `decision-maker/<acorpId>/act` with `treasury_transfer`: Direct financial transfers by a DDM.
    - `operator/acorp/<acorpId>/freeze-participant`, `freeze-outflows`: Ability to halt participant activity or treasury operations.
    These commands are dangerous in their impact but are explicitly documented as part of the intended functionality for specific, privileged roles within the A-Corp Foundry ecosystem.

## Hidden or Undocumented Functionality
None detected. The skill documentation is extensive and transparent about all exposed API endpoints and their functionalities, including the high-impact ones.

## Final Assessment
The A-Corp Foundry skill is classified as **BENIGN**.

The skill provides comprehensive API documentation for a platform designed to manage decentralized autonomous organizations (A-Corps). It details a wide range of functionalities, from basic participant interactions like creating A-Corps and voting, to highly privileged operator controls such as freezing participants, halting treasury outflows, and even permanently dissolving an A-Corp. It also includes mechanisms for direct on-chain smart contract interaction and financial transactions.

While many of these functionalities carry a high degree of risk if misused (e.g., financial loss, system disruption, irreversible destruction of an A-Corp), they are all explicitly documented as part of the platform's intended design. The documentation clearly outlines the roles (participants, operators, administrators) and the specific permissions associated with each, indicating a structured access control model. Furthermore, the skill describes built-in safety mechanisms like delegation constraints, risk score thresholds, and explicit warnings about the irreversible nature of certain actions.

There is no evidence of obfuscated code, hidden functionalities, or attempts to perform unauthorized actions like credential theft or data exfiltration to undeclared endpoints. The "dangerous" commands are transparently presented as legitimate tools for managing a complex, on-chain entity, particularly from the perspective of a human operator responsible for legal oversight and safety. The risk associated with this skill lies in the potential for a compromised or malicious actor to *abuse* these powerful, but legitimate, capabilities, rather than the skill itself being inherently malicious in its design or intent.

## Recommended Action
ALLOW

The skill is well-documented, transparent about its capabilities, and includes explicit warnings and role-based access controls for its high-impact functionalities. It is designed for managing complex decentralized organizations, which inherently involves powerful controls. The risk is manageable through proper access control, monitoring, and adherence to the documented behavioral rules by the agent and its human principal.