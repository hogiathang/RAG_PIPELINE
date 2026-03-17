from src.retrieval.retrieval import retrieve_similar_documents
from src.common.model.gemini_agent import GeminiAgent
from src.common.model.agent_adapter import AgentAdapter
from src.common.model.local_agent import LocalAgent
import json, re

def build_prompt_from_retrieve_similar_documents(user_prompt: str):
    pass

def format_json_response(response: str) -> json:
    clean_response = response.strip()
    cleaned = re.sub(r"^```json|^```|```$", "", clean_response).strip()

    match   = re.search(r"\{.*\}", cleaned, re.DOTALL)

    if match:
        json_str = match.group(0)
        return json.loads(json_str)
    else:
        raise ValueError("No valid JSON object found in the response.")

def extractor(file: str, file_content: str) -> dict:
    agent: AgentAdapter = LocalAgent()
    task_type = "agent-extractor"

    