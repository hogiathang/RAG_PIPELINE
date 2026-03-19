from src.retrieval.retrieval import retrieve_similar_documents
from src.common.model.gemini_agent import GeminiAgent
import json, re
from src.logging.log_manager import AppLogger

logger = AppLogger.get_logger(__name__)

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

    gemini_agent = GeminiAgent()

    response = gemini_agent.execute_task(skills_contents, "skills-analysis")

    logger.info(f"[INFO] Agent Analyzied Skill Raw Response {response}")

    formatted_response = format_json_response(response)

    search_queries = formatted_response.get("search_queries", [])

    search_contents = []

    for query in search_queries:
        search_result = retrieve_similar_documents(query)
        search_contents.extend(search_result)

    formatted_response["search_contents"] = search_contents
    logger.info(f"[INFO] Agent Analyzied Skill Formatted Response {formatted_response}")

    report = format_json_response(
        gemini_agent.execute_task(json.dumps(formatted_response), 
                                  "skills-report-generation"))
    
    logger.info(f"[INFO] Agent Generated Skill Report {report}")
    return report