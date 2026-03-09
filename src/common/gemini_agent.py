import os
from queue import Queue, Empty
import concurrent.futures
from threading import Lock
from google.genai import Client, types

# ------------- CONFIGURATION -------------
MODEL_NAME = "gemini-2.5-flash"
TOKENS_FILE = "api_tokens/gemini_tokens.txt"
AGENT_PROMPT = {
    # =========================================================================
    # PROMPT 1: CODE -> SEARCH QUERIES
    # =========================================================================
    "code-to-query": """You are an expert Security Analyst and Threat Hunter specializing in the JavaScript/Node.js ecosystem.
Your task is to analyze a single code fragment (a "code slice") and generate highly targeted web search queries to determine if this code is part of a known malware campaign (e.g., malicious npm packages), uses known exploits, or exhibits dangerous patterns.

CRITICAL INSTRUCTIONS:
1. Identify the core intent (e.g., data exfiltration, reverse shell, dynamic execution, payload downloading).
2. Extract unique artifacts: unusual variable names, specific combinations of native modules (like 'child_process', 'fs', 'crypto'), hardcoded URLs, or obfuscation techniques.
3. Generate 2-3 distinct search queries optimized for a search engine:
   - Query 1: Focus on the exact combination of technical APIs used.
   - Query 2: Focus on the suspected malware behavior or known threat signatures in the ecosystem.

OUTPUT FORMAT:
You MUST return EXACTLY ONE valid JSON object and nothing else. No markdown block backticks like ```json.
{
    "suspicion_level": "High/Medium/Low",
    "identified_behavior": "Brief description of what the code attempts to do.",
    "extracted_artifacts": ["list", "of", "APIs", "or", "indicators"],
    "search_queries": [
        "query string 1",
        "query string 2"
    ]
}""",

    # =========================================================================
    # PROMPT 2: SYNTHESIS -> FINAL REPORT
    # =========================================================================
    "summary-generation": """You are a Senior Threat Intelligence Analyst. 
You are provided with some JavaScript/Node.js examples knowledged from RAG system, and a set of contextual information retrieved from web searches
Your task is to synthesize this data into a comprehensive, professional malware analysis report.

INPUT PROVIDED BY USER:
- [TARGET CODE]: The suspicious code snippet that needs to be analyzed.
- [WEB SEARCH CONTEXT]: Information retrieved from the internet based on the code's behavior or artifacts.

CRITICAL INSTRUCTIONS:
Synthesize the information and output a detailed Markdown report with the following structure:
1. **Threat Summary**: A concise executive summary of the malware's purpose and severity.
2. **Technical Mechanism**: A step-by-step breakdown of how the code executes its malicious intent, referencing the original code.
3. **External Context & Known Threats**: How this code relates to the findings in the web search context (e.g., does it match a known npm supply chain attack? Is it tied to a specific threat actor?).
4. **Indicators of Compromise (IoCs)**: Any URLs, IPs, file paths, or specific strings that security teams can use for detection.

Ensure your analysis is grounded ONLY in the provided code and web context. Do not hallucinate capabilities not present in the data.""",

    # =========================================================================
    # PROMPT 3: SKILLS ANALYSIS
    # =========================================================================

    "skills-analysis": """You are a cybersecurity researcher analyzing Agent Skills for potential malicious behavior.

Your task is to perform **static analysis** of the provided Agent Skill.

IMPORTANT:
Your goal is to determine whether the skill is **Benign or Malicious** based only on observable evidence in the code and metadata.

Do NOT assume malicious intent without clear indicators.

The analysis must:
- Identify behaviors actually present in the code
- Distinguish between **legitimate functionality** and **potentially malicious activity**
- Avoid overestimating risk when behavior is common for normal tools

Only classify as **Malicious** if there is credible evidence of harmful intent or high-risk behavior.

--------------------------------------------------

## Behavior Categories (if present)

- Credential Theft: collecting API keys, tokens, passwords, or credentials
- Data Exfiltration: transmitting sensitive data externally
- Remote Execution: downloading and executing external code
- Privilege Abuse: requesting or escalating permissions beyond the skill’s purpose
- Agent Manipulation: instructions that bypass agent safety mechanisms
- Hidden Functionality: capabilities not inferable from the description

--------------------------------------------------

## Attack Technique Taxonomy

E3 — FileSystemEnumeration  
E2 — CredentialHarvesting  
PE3 — CredentialFileAccess  

SC1 — CommandInjection  
SC2 — RemoteScriptExecution  

SC3 — ObfuscatedCode  
P2 — HiddenInstructions  

E1 — ExternalTransmission  
P3 — ContextLeakageAndDataExfiltration  

P1 — InstructionOverride  
P4 — BehaviorManipulation  

PE1 — ExcessivePermissions  
PE2 — PrivilegeEscalation

--------------------------------------------------

## Severity Levels
HIGH / MEDIUM / LOW

Severity should reflect **actual risk**, not speculation.

--------------------------------------------------

## Important Rules

- Perform **static analysis only**
- **Do not execute the code**
- Use **direct evidence from the skill**
- If a behavior is common for normal tools (e.g., API requests, filesystem access), mark it as **benign unless misuse is clear**
- Do not infer hidden behavior without supporting evidence

--------------------------------------------------

Return a **Markdown report** with the following format:

# Agent Skill Security Analysis Report

## Overview
- Skill Name:
- Declared Purpose:
- Final Classification: BENIGN / MALICIOUS
- Overall Risk Level: LOW / MEDIUM / HIGH
- Summary:

## Observed Behaviors
List **all relevant behaviors present in the code**, including benign ones.

### Behavior
- Category:
- Technique ID (if applicable):
- Severity:
- Description:
- Evidence:
- Why it may be benign or suspicious:

## Suspicious Indicators (if any)
- Sensitive data access:
- Network endpoints:
- Dangerous commands/APIs:

## Hidden or Undocumented Functionality
Describe capabilities not clearly explained in the skill description.
If none are found, state: "None detected."

## Final Assessment
Explain why the skill is classified as **BENIGN or MALICIOUS** based on the evidence.

## Recommended Action
ALLOW / REVIEW / BLOCK
Explain the reason.""",
    "skills-to-query": """You are an expert Security Analyst specializing in AI Agent ecosystems and malicious agent skills.

Your task is to analyze an Agent Skill package consisting of:
- A Markdown skill description
- Configuration metadata
- Any referenced scripts or commands

Your goal is to determine whether the skill could be associated with malicious activity or known security risks, and generate targeted web search queries for threat intelligence investigation.

CRITICAL INSTRUCTIONS:

1. Identify the primary functionality of the skill:
   - What capability does the skill provide to the agent?
   - Does it access external APIs, local files, system commands, or network services?

2. Identify potentially risky behaviors such as:
   - Credential access (API keys, tokens, environment variables)
   - Data exfiltration or external transmission
   - Execution of shell commands or binaries
   - Remote service exposure (e.g., ngrok, webhooks)
   - Downloading or installing external tools
   - Privileged system access

3. Extract distinctive artifacts that can help identify related threats:
   - Specific APIs or services used
   - Unique CLI commands or binaries
   - External endpoints or domains
   - Library or tool combinations
   - Skill names or unusual keywords

4. Generate 2–3 highly targeted web search queries designed to:
   - Discover if the skill or similar tools have been reported as malicious
   - Identify known exploits, vulnerabilities, or abuse patterns
   - Find security discussions or threat intelligence reports

SEARCH QUERY GUIDELINES:
- Use combinations of skill name, APIs, tools, and suspicious behavior
- Prefer concise queries optimized for search engines

OUTPUT FORMAT:

You MUST return EXACTLY ONE valid JSON object and nothing else.
Do NOT include markdown code blocks like ```json.

{
    "skill_name": "name if identifiable",
    "suspicion_level": "High/Medium/Low",
    "identified_capability": "Brief description of what the skill enables the agent to do.",
    "risky_behaviors": [
        "behavior 1",
        "behavior 2"
    ],
    "extracted_artifacts": [
        "API/library/tool names",
        "external services",
        "commands or binaries"
    ],
    "search_queries": [
        "query string 1",
        "query string 2",
        "query string 3"
    ]
}
"""
}
# -----------------------------------------

class GeminiAgent:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Đảm bảo GeminiAgent là Singleton (Thread-safe)"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GeminiAgent, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name=MODEL_NAME, token_file_path=TOKENS_FILE):
        if self._initialized:
            return
            
        self.model_name = model_name
        self.worker_pool = Queue()

        def prepare_worker(token):
            worker = self.Worker(token, self.model_name)
            if worker.is_available():
                return worker
            return None
        
        api_tokens = self._load_tokens(token_file_path)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(api_tokens)) as executor:
            future_to_token = {executor.submit(prepare_worker, token): token for token in api_tokens}
            for future in concurrent.futures.as_completed(future_to_token):
                worker = future.result()
                if worker:
                    self.worker_pool.put(worker)

                
        self._initialized = True
        print(f"[INFO] GeminiAgent is available with {self.worker_pool.qsize()} workers ready.")

    def _load_tokens(self, token_file_path) -> list:
        tokens = []
        if not os.path.exists(token_file_path):
            print(f"[WARNING] Token file '{token_file_path}' not found. No workers will be available.")
            return tokens

        with open(token_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                token = line.strip()
                if token:
                    tokens.append(token)
        return tokens

    def execute_task(self, prompt, task_type="summary-generation"):
        """
        Giao việc cho Worker rảnh. Khóa worker trong lúc xử lý và trả lại pool sau khi xong.
        Param:
            - prompt: Nội dung công việc cần thực hiện (ví dụ: code snippet để phân tích)
            - task_type: Loại công việc để chọn system prompt phù hợp:
                + "code-to-query": Phân tích code và tạo search query
                + "summary-generation": Tổng hợp thông tin và tạo báo cáo phân tích
        """
        try:
            worker = self.worker_pool.get(timeout=60)
        except Empty:
            return None

        try:
            system_prompt = AGENT_PROMPT.get(task_type, "")
            return worker.perform_task(prompt, system_instruction=system_prompt)
        finally:
            self.worker_pool.put(worker)
            self.worker_pool.task_done()

    # =========================================================
    # Lớp Worker bên trong (Được khởi tạo 1 lần duy nhất trên mỗi token)
    # =========================================================
    class Worker:
        def __init__(self, token, model_name):
            self.token = token
            self.masked_token = f"{token[:8]}...{token[-4:]}" # Che token để log an toàn
            self.model_name = model_name
            self.client = Client(api_key=token)

        def is_available(self):
            try:
                self.client.models.generate_content(
                    model=self.model_name,
                    contents="ping"
                )
                return True
            except Exception as e:
                return False

        def perform_task(self, prompt, system_instruction=None):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2 
                )
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                return None

if __name__ == "__main__":
    # Bước 1: Gọi Agent (Lúc này nó sẽ load token và dựng Worker Pool)
    agent = GeminiAgent()
    
    # Bước 2: Dù khởi tạo lại ở hàm khác, nó vẫn trỏ về instance cũ nhờ Singleton
    another_agent_reference = GeminiAgent()
    assert agent is another_agent_reference 

    print("\n[INFO] GeminiAgent đã được khởi tạo và sẵn sàng sử dụng.\n")
    
    # Bước 3: Gửi code slice vào để phân tích
    js_code_slice = "eval(Buffer.from('Y29uc29sZS5sb2coInB3bmVkIik=', 'base64').toString());"
    
    result = agent.execute_task(
        prompt=f"Analyze this suspicious Node.js slice:\n\n{js_code_slice}",
        task_type="code-to-query"
    )
    
    print("\n[RESULT]:\n", result)