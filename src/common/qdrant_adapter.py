from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Query
from src.common.embedding_model import EmbeddingModel
from src.common.web_search_engine import WebSearchEngine

class QdrantAdapter:
    _instance = None
    def __new__(cls):
        if cls._instance == None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, url="http://localhost:6333", collection="malware", dim=1536):
        self.client = QdrantClient(url=url,timeout=30)
        self.collection = collection
        self.embedding_model = EmbeddingModel()
        if not self.client.collection_exists(collection_name=collection):
            self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
            )

    def insert(self, ids, vectors, payloads, batch_size=100):
        total = len(ids)

        for start in range(0, total, batch_size):
            end = start + batch_size

            batch_points = [
                PointStruct(
                    id=ids[i],
                    vector=vectors[i],
                    payload=payloads[i]
                )
                for i in range(start, min(end, total))
            ]

            self.client.upsert(
                collection_name=self.collection,
                points=batch_points
            )

            print(f"Inserted batch {start} → {min(end, total)}")


    def _search(self, question , top_k : int = 5) -> list[str]:
        query_vector = self.embedding_model.embed(question)
        results = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=top_k,
            with_payload=True
        )
        points = results.points
        contexts: list[str] = []
        
        for r in points:
            payload = getattr(r,"payload",None) or {}
            text = payload.get("text", "")
            source = payload.get("source","")
            if text:
                contexts.append(f"[SOURCE: {source}]\n{text}")

        return contexts

    def search(self,question: str, top_k : int = 5) -> list[str]:
        result = self._search(question, top_k)
        
        search_engine = WebSearchEngine()
        web_searh_response = search_engine.search(question)

        return result + web_searh_response

    def delete(self):
        self.client.delete_collection(self.collection)