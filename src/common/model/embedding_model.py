"""
Class Embedding Model for RAG System

Function:
    - Khởi tạo embedding model
    + Gọi hàm embedding để embed text / code


Singleton Pattern    
"""


from threading import Lock
from sentence_transformers import SentenceTransformer
from typing import List, Union

EMBEDDING_MODEL_CONFIG = {
    "provider": "huggingface",
    "model_name": "BAAI/bge-code-v1",
    "device":"cpu", #"cuda" if torch.cuda.is_available() else "cpu",
    "normalize_embeddings": True,
    "batch_size": 32,
    "max_length": 512
}


class EmbeddingModel:
    _instance = None
    _lock: Lock = Lock()

    def __new__(cls):
        """
        Load model
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(EmbeddingModel, cls).__new__(cls)
                cls._instance._initialize_model()

        return cls._instance

    def _initialize_model(self):
        """
        Initialize the embedding model based on the configuration.
        """
        self.model = SentenceTransformer(
            EMBEDDING_MODEL_CONFIG["model_name"],
            device=EMBEDDING_MODEL_CONFIG["device"]
        )

        self.model.max_seq_length = EMBEDDING_MODEL_CONFIG["max_length"]
        self.normalize_embeddings = EMBEDDING_MODEL_CONFIG["normalize_embeddings"]
        self.batch_size = EMBEDDING_MODEL_CONFIG["batch_size"]

    def embed(self, codes: Union[List[str], str]) -> Union[List[List[float]], List[float]]:
        """
        Generate embeddings for a list of texts or a single text.
        """
        if isinstance(codes, str):
            codes = [codes]

        embeddings = self.model.encode(
            codes,
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize_embeddings,
            show_progress_bar=True
        )

        if len(embeddings) == 1:
            return embeddings[0]
        return embeddings