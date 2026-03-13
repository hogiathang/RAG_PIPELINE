from src.retrieval.retrieval import retrieve_similar_documents
from src.common.gemini_agent import GeminiAgent
import json, re

def build_summary_generation(user_prompt: str, documents: list[str]) -> str:
    gemini_agent = GeminiAgent()
    
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [LOCAL KNOWLEDGE AND WEB SEARCH CONTENT]:
        {"\n\n".join(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "summary-generation")

def build_skills_analysis_generation(user_prompt: str, documents: list[str]) -> json:
    gemini_agent = GeminiAgent()
    
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [LOCAL KNOWLEDGE AND WEB SEARCH CONTENT]:
        {"\n\n".join(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "skills-analysis")

def build_prompt_from_retrieve_similar_documents(user_prompt: str):
    pass
    # similar_documents = retrieve_similar_documents(build_query_prompt(user_prompt))

    # return build_summary_generation(user_prompt, similar_documents)

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
        gemini_agent.execute_task(json.dumps(formatted_response), 
                                  "skills-report-generation"))
    
    print(f"[INFO] Agent Analyzied Skill Report {report}")
    return report