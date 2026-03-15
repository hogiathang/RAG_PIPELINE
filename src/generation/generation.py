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

def build_prompt_from_retrive_similar_documents_for_skills_analysis(skills_contents: str) -> json:

    agent: AgentAdapter = LocalAgent()

    response = agent.execute_task(skills_contents, "skills-analysis")

    print(f"[INFO] Agent Analyzied Skill Response {response}")

    formatted_response = format_json_response(response)

    search_queries = formatted_response.get("search_queries", [])

    search_contents = []

    for query in search_queries:
        search_result = retrieve_similar_documents(query)
        search_contents.extend(search_result)

    formatted_response["search_contents"] = search_contents
    print(f"[INFO] Agent Analyzied Skill Formatted Response {formatted_response}")

    report = format_json_response(
        agent.execute_task(json.dumps(formatted_response), 
                                  "skills-report-generation"))
    
    print(f"[INFO] Agent Analyzied Skill Report {report}")
    return report