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

def retrieve_similar_documents(question : str) -> list[str]:
    logger.info(f"Retrieving top {TOP_K} similar documents for the question: {question}")
    qdrantDB = QdrantAdapter()
    return qdrantDB.search(question,TOP_K)