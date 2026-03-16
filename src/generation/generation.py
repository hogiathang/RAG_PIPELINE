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


def analyze_skills_file(skills_contents: str, using_local_model: bool) -> json:

    print(f"[INFO] Analyze skill content: {skills_contents}")

    agent: AgentAdapter = LocalAgent() if using_local_model else GeminiAgent()

    response = agent.execute_task(skills_contents, "skills-analysis-agent")

    print(f"{"="*60}")
    print(response)

    return json.loads(response)

def analyze_package_codes(contents: list[str], using_large_language_model: bool) -> json:

    if not contents:
        return {}

    agent: AgentAdapter = LocalAgent()
    combined_contents = "\n\n".join(contents)

    agent: AgentAdapter = LocalAgent() if not using_large_language_model else GeminiAgent()

    response = agent.execute_task(combined_contents, "source-code-analysis")

    print(f"{"="*60}")
    print(f"ANALYZED SOURCE CODE: {response}")

    return json.loads(response)

def verify_result(result: json) -> json:
    agent: AgentAdapter = GeminiAgent()

    evaluation = agent.execute_task(json.dumps(result), "skills-eval")

    print(f"{"="*60}")
    print(f"EVALUATION RESULT: {evaluation}")
    
    start_idx = evaluation.find("{")
    end_idx = evaluation.rfind("}")

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        json_str = evaluation[start_idx:end_idx+1]
        return json.loads(json_str)
    else:
        print("[ERROR] No valid JSON object found in the evaluation response.")