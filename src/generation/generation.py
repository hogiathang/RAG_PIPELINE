from src.retrieval.retrieval import retrieve_similar_documents_for_questions
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

    response = format_json_response(response)
    search_queries = response.get("search_queries", [])
    queries_results = retrieve_similar_documents_for_questions(search_queries)
    response["search_contents"] = queries_results

    logger.info(f"[INFO] Agent Analyzied Skill Formatted Response {response}")

    report = format_json_response(
        agent.execute_task(json.dumps(response), 
                                  "skills-report-generation"))
    
    logger.info(f"[INFO] Agent Generated Skill Report {report}")

    return report