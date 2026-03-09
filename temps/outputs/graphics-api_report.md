# Agent Skill Security Analysis Report

## Overview
- Skill Name: graphics-api-hooking
- Declared Purpose: Guide for graphics API hooking and rendering techniques for DirectX, OpenGL, and Vulkan. Use this skill when working with graphics hooks, overlay rendering, shader manipulation, or game rendering pipeline analysis.
- Final Classification: MALICIOUS
- Overall Risk Level: HIGH
- Summary: This skill provides a comprehensive guide, including code examples, for graphics API hooking, overlay rendering, shader manipulation (specifically "wallhacks" and "chams"), and anti-detection techniques. While presented as a "guide," the detailed instructions and explicit examples of game cheats, combined with the focus on evading detection and sourcing information from a known game hacking repository, indicate a high potential for misuse in malicious contexts.

## Observed Behaviors

### Behavior: API Hooking and Process Injection
- Category: Privilege Abuse / Agent Manipulation
- Technique ID: P4 — BehaviorManipulation, SC1 — CommandInjection
- Severity: HIGH
- Description: The skill details how to hook graphics APIs (DirectX, OpenGL, Vulkan) using VTable hooking and other methods. This technique allows for injecting code into other processes to alter their behavior or extract information.
- Evidence: Code snippets for `IDirect3DDevice9::EndScene`, `IDXGISwapChain::Present`, `wglSwapBuffers`, `vkQueuePresentKHR` hooking, and explicit VTable hooking examples (`oPresent = (Present)swapChainVtable[8];`).
- Why it may be benign or suspicious: Benign uses include legitimate debugging, performance analysis, or creating benign overlays. However, it is a fundamental technique for process injection, bypassing security mechanisms (like anti-cheat), and altering application behavior without consent, which is highly suspicious.

### Behavior: Overlay Rendering and UI Manipulation
- Category: Agent Manipulation
- Technique ID: P4 — BehaviorManipulation
- Severity: MEDIUM
- Description: The skill describes various methods for rendering custom overlays, including using ImGui, creating external transparent windows, hooking the Desktop Window Manager (DWM), and hijacking existing overlays like Steam or NVIDIA GeForce Experience.
- Evidence: `ImGui_ImplDX11_Init`, `ImGui::Begin("Overlay")`, `Create transparent window`, `Set WS_EX_LAYERED | WS_EX_TRANSPARENT`, `Hook Desktop Window Manager`, `Hook Steam's overlay functions`, `Hook GeForce Experience overlay`.
- Why it may be benign or suspicious: Benign for legitimate in-game information displays (e.g., FPS counters). Suspicious because these techniques can be used for phishing, injecting malicious UI elements, or obscuring legitimate application interfaces.

### Behavior: Shader Manipulation for Game Cheats
- Category: Agent Manipulation
- Technique ID: P4 — BehaviorManipulation
- Severity: HIGH
- Description: The skill provides explicit code examples and techniques for implementing "Wallhack" and "Chams" (character highlighting) through shader manipulation. These are well-known game cheating techniques.
- Evidence: `OMSetDepthStencilState(depthDisabledState, 0);`, `return float4(1, 0, 0, 0.5); // Red transparent` (for wallhack), `if (isEnemy) { return float4(1, 0, 0, 1); }` (for chams).
- Why it may be benign or suspicious: This is a direct instruction and code example for implementing game cheats, which is inherently malicious in the context of fair play and application integrity.

### Behavior: Anti-Detection and Evasion Techniques
- Category: Agent Manipulation
- Technique ID: P4 — BehaviorManipulation
- Severity: HIGH
- Description: The skill discusses methods to detect API hooks and provides "Evasion Techniques" such as "Trampoline hooks," "Hardware breakpoints," and "Timing obfuscation" to bypass security measures.
- Evidence: `VTable integrity checks`, `Code section verification`, `Call stack analysis` (for detection), `Trampoline hooks`, `Hardware breakpoints`, `Timing obfuscation` (for evasion).
- Why it may be benign or suspicious: While understanding detection is part of security research, providing explicit "evasion techniques" in the context of game hacking strongly suggests an intent to bypass security systems (e.g., anti-cheat software), which is a malicious activity.

### Behavior: External Data Retrieval from Game Hacking Repository
- Category: Data Exfiltration (potential source of malicious content)
- Technique ID: E1 — ExternalTransmission (for retrieval, not transmission)
- Severity: MEDIUM
- Description: The skill instructs the agent to fetch detailed information, including code snapshots, from the `gmh5225/awesome-game-security` GitHub repository. This repository is explicitly identified in the web search context as containing tools for game security, hacking, and anti-cheat.
- Evidence: URLs like `https://raw.githubusercontent.com/gmh5225/awesome-game-security/refs/heads/main/README.md`, `https://raw.githubusercontent.com/gmh5225/awesome-game-security/refs/heads/main/archive/{owner}/{repo}.txt`.
- Why it may be benign or suspicious: While fetching external documentation can be benign, the specific source is a known collection of game hacking tools. Directing the agent to retrieve and process information from such a source significantly increases the risk that the agent could be used to understand, generate, or facilitate malicious code.

## Suspicious Indicators
- Sensitive data access: No direct access to sensitive data is present in the skill's code. However, the described techniques (API hooking, overlay rendering) could be leveraged to steal credentials or exfiltrate data if combined with other malicious functionalities.
- Network endpoints: `https://raw.githubusercontent.com/gmh5225/awesome-game-security/...` (a repository known for game hacking tools).
- Dangerous commands/APIs: `IDirect3DDevice9::EndScene`, `IDXGISwapChain::Present`, `wglSwapBuffers`, `vkQueuePresentKHR` (hooking points for process injection), `Create transparent window`, `SetLayeredWindowAttributes`, `Hook Desktop Window Manager`, `Hook Steam's overlay functions`, `Hook GeForce Experience overlay` (for UI manipulation), `OMSetDepthStencilState` (for shader manipulation), `CallWindowProc` (for `WndProc` hooking).

## Hidden or Undocumented Functionality
None detected. The skill's content directly aligns with its declared purpose of providing a guide for graphics API hooking and rendering techniques. However, the *nature* of these techniques and their explicit examples (game cheats, anti-detection) are highly suspicious.

## Final Assessment
The skill is classified as **MALICIOUS**. While it presents itself as a "guide," its content is overwhelmingly focused on techniques that are primarily used for malicious purposes, specifically game cheating and bypassing security mechanisms. The skill provides explicit code examples for "wallhacks" and "chams," details methods for API hooking and process injection, and discusses "anti-detection" and "evasion techniques." Furthermore, it instructs the agent to retrieve additional information and code from a GitHub repository known for game hacking tools. This combination of detailed instructions for harmful activities and the sourcing of related content makes the skill a tool for enabling malicious behavior.

## Recommended Action
BLOCK
This skill provides detailed instructions and code examples for techniques that are inherently high-risk and commonly associated with malicious activities such as game cheating, process injection, and bypassing security systems. Allowing this skill could enable an agent to understand, generate, or facilitate malicious code and actions.