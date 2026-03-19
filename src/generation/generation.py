from src.retrieval.retrieval import retrieve_similar_documents
from src.common.model.gemini_agent import GeminiAgent
from src.common.model.agent_adapter import AgentAdapter
from src.common.utils import format_json_response
from src.logging.log_manager import AppLogger
import json

logger = AppLogger.get_logger(__name__)

def generate_report_from_skill_package(skills_contents: str) -> json:

    agent: AgentAdapter = GeminiAgent()

    response = agent.execute_task(skills_contents, "skills-analysis")

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
        agent.execute_task(json.dumps(formatted_response), 
                                  "skills-report-generation"))
    
    logger.info(f"[INFO] Agent Generated Skill Report {report}")
    return report