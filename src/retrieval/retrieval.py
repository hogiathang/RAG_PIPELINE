"""
Retrieval TOP K SIMILAR FROM VECTOR SEARCH
"""

from src.common.qdrant_adapter import QdrantAdapter

TOP_K = 5

def build_query_prompt(code: str) -> str:
    prompt = f"""Analyze the following Javascript code snippet \n{code}"""
    return prompt.strip()

def build_query_prompt_for_skills_analysis(code: str) -> str:
    prompt = f"""Analyze the following agent's skills behavior based on the Javascript code snippet \n{code}"""
    return prompt.strip()


def retrieve_similar_documents(question : str) -> list[str]:
    print(f"[INFO] Retrieving similar documents for question")
    qdrantDB = QdrantAdapter()
    return qdrantDB.search(question,TOP_K)