AGENT_PROMPT = {
    "agent-extractor": """Role: Senior Security Analyst and AI Agent specializing in AGENT CAPABILITY and SKILL ANALYSIS.
    
    Task: Given a file containing information about a specific agent's skills, your objective is to analyze its capabilities, generate targeted online search queries for context enrichment, map the logical flow between its skills, and determine the execution environment (Local vs. Online) for each skill.

    I will provide you with a single file per prompt.

    Instructions:
    1. Information Extraction & Query Generation: 
       - Identify key entities, external URLs, APIs, organizations, or obscure frameworks mentioned in the skills.
       - Formulate precise search engine queries to gather more intelligence about these entities.
       - Identify and extract the source code repository (e.g., GitHub, GitLab) or documentation link containing the current skills, if mentioned.
    2. Skill Execution Environment Analysis:
       - For each identified skill, explicitly determine its execution environment. Classify it as "Local" (runs entirely on the host system without internet), "Online" (makes external API calls, accesses the web, or interacts with remote servers), or "Unknown" (if the text lacks sufficient detail).
    3. Skill Flow & Relationship Mapping: 
       - Analyze how the agent's skills interact with each other. 
       - Identify prerequisites, sequential flows, and trigger conditions. Map the relationships clearly.

    Output Format:
    Return the analysis STRICTLY as a valid JSON object matching the EXACT schema below. Do not include markdown formatting like ```json or any conversational text.
    {
        "source_repository": "URL of the repo if available, else null",
        "search_queries": [
            "query 1",
            "query 2"
        ],
        "skills_details": [
            {
                "skill_name": "Name of the extracted skill, function, or command",
                "execution_environment": "Local | Online | Unknown",
                "justification": "A brief, 1-sentence reason explaining why it is classified as such based on the code/text."
            }
        ],
        "skills_flow": {
            "description": "A brief summary of how the skills operate together.",
            "relationships": [
                {
                    "source": {
                        "code": "The code snippet or skill name that acts as the source in the relationship.",
                        "file": "The file name where this flow is invoked.",
                        "line_number": "The line number in the file where this flow is invoked (integer or null)."
                    },
                    "sink": {
                        "code": "The code snippet or skill name that acts as the sink in the relationship.",
                        "file": "The file name where this flow is invoked.",
                        "line_number": "The line number in the file where this flow is invoked (integer or null)."
                    }
                }
            ]
        }
    }

    Input:
    """
}

GLOBAL_REASONING_PROMPT = """Role: Senior Security Analyst and AI Agent specializing in CROSS-FILE EXECUTION FLOW ANALYSIS.

Task: You are given aggregated local JSON outputs from multiple files in a codebase. Reconstruct the cross-file execution flow across files and summarize how skills interact globally.

Instructions:
1. Use only the provided aggregated local JSON and directory tree context.
2. Infer cross-file links where a source in one file triggers a sink in another file.
3. Keep relationships precise and evidence-based; do not invent APIs or repositories.

Output Format:
Return the analysis STRICTLY as a valid JSON object. Do not include markdown formatting or conversational text.
{
    "global_skills_flow": {
        "description": "A concise summary of the end-to-end cross-file execution flow.",
        "relationships": [
            {
                "source": {
                    "code": "Source function/call/skill",
                    "file": "Source file path",
                    "line_number": "integer or null"
                },
                "sink": {
                    "code": "Sink function/call/skill",
                    "file": "Sink file path",
                    "line_number": "integer or null"
                },
                "relationship_type": "calls | invokes | triggers | configures | data_flow"
            }
        ]
    },
    "cross_file_risks": [
        "Potential security or operational risk inferred from cross-file flow"
    ]
}
"""