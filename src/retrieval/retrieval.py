"""
Retrieval TOP K SIMILAR FROM VECTOR SEARCH
"""

from src.ingestion.qdrant_adapter import QdrantAdapter
from src.logging.log_manager import AppLogger

logger = AppLogger.get_logger(__name__)
TOP_K = 5

def build_query_prompt(code: str) -> str:
    prompt = f"""Analyze the following Javascript code snippet \n{code}"""
    return prompt.strip()

def retrieve_similar_documents_for_questions(questions : list[str]) -> list[str]:
    result = []
    
    for question in questions:
        logger.info(f"Retrieving top {TOP_K} similar documents for the question: {question}")
        qdrantDB = QdrantAdapter()
        similar_docs = qdrantDB._search(question,TOP_K)
        result.extend(similar_docs)

    return result