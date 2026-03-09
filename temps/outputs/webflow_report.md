# Agent Skill Security Analysis Report

## Overview
- Skill Name: webflow
- Declared Purpose: Webflow integration patterns for this boilerplate. Use when setting up data attributes, connecting Webflow HTML to the JS/WebGL layer, configuring the preloader, or troubleshooting Webflow-specific issues.
- Final Classification: BENIGN
- Overall Risk Level: LOW
- Summary: This skill is a descriptive document outlining a legitimate integration pattern for a custom JavaScript/WebGL application with a Webflow-hosted website. It provides detailed instructions for structuring HTML, loading a JavaScript bundle, and configuring various interactive elements and animations. No malicious behaviors or high-risk activities are present in the skill's definition.

## Observed Behaviors

### Behavior: External Script Loading Instructions
- Category: N/A (Common Web Development Practice)
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill provides instructions for injecting a custom JavaScript bundle (`main.js`) into a Webflow site via a `<script>` tag. It specifies example URLs for both production (CDN) and development (localhost) environments.
- Evidence:
    ```html
    <script src="https://your-cdn.com/main.js"></script>
    <script src="http://localhost:3000/src/main.js"></script>
    ```
- Why it may be benign or suspicious: This is a benign and standard practice for deploying web applications. The risk is not in the instruction itself, but in the trustworthiness of the actual JavaScript file loaded from the specified URL, which is outside the scope of this skill's static analysis.

### Behavior: DOM Interaction and Manipulation Instructions
- Category: N/A (Common Web Development Practice)
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill extensively details the use of `data-*` attributes to connect Webflow HTML elements to the custom JavaScript/WebGL layer. These attributes are used for page routing, WebGL element identification, preloader configuration, and various scroll animations.
- Evidence: `data-page`, `data-taxi-view`, `data-gl`, `data-loader`, `data-anim`, `data-lenis-prevent` attributes are described throughout the document.
- Why it may be benign or suspicious: This is a benign and standard method for JavaScript to interact with and control elements within an HTML document.

### Behavior: Single-Page Application (SPA) Navigation Instructions
- Category: N/A (Common Web Development Practice)
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill explains how `Taxi.js` is used to intercept internal links for smooth SPA navigation, while allowing external or specifically ignored links to trigger full page loads.
- Evidence: "Taxi intercepts all links except: `a:not([target]):not([href^=\\#]):not([data-taxi-ignore])`"
- Why it may be benign or suspicious: This is a benign and common feature in modern web applications to enhance user experience.

### Behavior: Build Process Description
- Category: N/A (Common Development Workflow)
- Technique ID (if applicable): N/A
- Severity: LOW
- Description: The skill mentions the command `bun run build` to compile the JavaScript source files into a single IIFE bundle (`dist/main.js`).
- Evidence: `bun run build → dist/main.js`
- Why it may be benign or suspicious: This is a benign and standard instruction for a web development build process.

## Suspicious Indicators
- Sensitive data access: None. The skill is purely descriptive and does not contain any code or instructions to access sensitive data.
- Network endpoints: The skill mentions `https://your-cdn.com/main.js` and `http://localhost:3000/src/main.js` as *example* locations for a JavaScript bundle. These are not endpoints *accessed by the skill itself*, but rather instructions for where a user's custom JavaScript should be hosted.
- Dangerous commands/APIs: None. All mentioned APIs (`window.Webflow.push()`, DOM manipulation via `data-*` attributes) are standard for web development and are presented in a benign context.

## Hidden or Undocumented Functionality
None detected. The skill is a detailed and transparent documentation of an integration pattern, with all capabilities clearly explained.

## Final Assessment
The skill is classified as **BENIGN**. It is a comprehensive documentation file that describes how to integrate a custom JavaScript/WebGL application with a Webflow-hosted website. The content focuses on legitimate web development practices, including DOM manipulation via data attributes, SPA navigation, and build processes. There is no executable code within the skill itself, nor does it contain any instructions that suggest malicious intent, such as credential theft, data exfiltration, remote execution, or privilege abuse. The potential for security risks would stem from the actual JavaScript code implemented by the user following these patterns, or the security of the hosting environment for that JavaScript, neither of which is part of this skill's static analysis.

## Recommended Action
ALLOW
The skill is purely descriptive documentation and does not pose any direct security threat. It outlines standard web development integration patterns.