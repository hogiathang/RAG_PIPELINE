from src.retrieval.retrieval import retrieve_similar_documents
from src.common.gemini_agent import GeminiAgent
import json

def build_summary_generation(user_prompt: str, documents: list[str]) -> str:
    gemini_agent = GeminiAgent()
    
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [WEB SEARCH CONTEXT]:
        {"\n\n".join(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "summary-generation")

def build_skills_analysis_generation(user_prompt: str, documents: list[str]) -> json:
    gemini_agent = GeminiAgent()
    
    final_prompt = f"""[TARGET CODE]:
        {user_prompt}

        [WEB SEARCH CONTEXT]:
        {"\n\n".join(documents)}
    """

    return gemini_agent.execute_task(final_prompt, "skills-analysis")

def build_prompt_from_retrieve_similar_documents(user_prompt: str):
    pass
    # similar_documents = retrieve_similar_documents(build_query_prompt(user_prompt))

    # return build_summary_generation(user_prompt, similar_documents)

def build_prompt_from_retrive_similar_documents_for_skills_analysis(skills_contents: str):

    gemini_agent = GeminiAgent()

    similar_docs = retrieve_similar_documents(skills_contents)

    return build_skills_analysis_generation(skills_contents, similar_docs)