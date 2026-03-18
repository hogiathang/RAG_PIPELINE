import os
import uuid
import json

from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.common.embedding_model import EmbeddingModel
from src.common.qdrant_adapter import QdrantAdapter
from pathlib import Path

INPUT_DIR = "./backup_rag"

def load_checker() -> list:

    checker_file = "./checker.json"

    if not os.path.exists(checker_file):
        print(f"[INFO] Checker file '{checker_file}' not found. Starting with an empty list.")
        return []

    try:
        with open(checker_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("checks", [])
    except Exception as e:
        print(f"[ERROR] Failed to load checker file: {e}")
        return []


def load_document(file_path: str):
    """Load document based on file type"""

    try:

        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            return loader.load()

        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
            return loader.load()

        elif file_path.endswith(".json"):

            try:
                loader = JSONLoader(
                    file_path=file_path,
                    jq_schema=".",
                    text_content=False
                )
                return loader.load()

            except Exception:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                return [
                    Document(
                        page_content=json.dumps(data, ensure_ascii=False),
                        metadata={"source": file_path}
                    )
                ]

        else:
            return None

    except Exception as e:
        print(f"Load error {file_path}: {e}")
        return None


def normalize_vectors(vectors):
    """
    Convert embedding output to list[list[float]] for Qdrant
    """

    # numpy array -> list
    if hasattr(vectors, "tolist"):
        vectors = vectors.tolist()

    # single vector -> wrap
    if isinstance(vectors, list) and len(vectors) > 0 and isinstance(vectors[0], float):
        vectors = [vectors]

    # ensure python float
    normalized = []
    for v in vectors:
        if hasattr(v, "tolist"):
            v = v.tolist()
        normalized.append([float(x) for x in v])

    return normalized


def ingest_data():

    qdrant_db = QdrantAdapter()
    embedding_model = EmbeddingModel()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    checked_files = load_checker()

    total_vectors = 0
    total_files = 0

    for root, dirs, files in os.walk(INPUT_DIR):

        if files in checked_files:
            print(f"[SKIP] Already ingested files in {root}. Skipping...")
            continue

        for file in files:

            file_path = os.path.join(root, file)

            documents = load_document(file_path)

            if not documents:
                continue

            try:

                components = text_splitter.split_documents(documents)

                if len(components) == 0:
                    continue

                texts = [doc.page_content for doc in components]

                # embedding
                vectors = embedding_model.embed(texts)

                # FIX VECTOR FORMAT
                vectors = normalize_vectors(vectors)

                ids = [str(uuid.uuid4()) for _ in texts]

                payloads = [
                    {
                        "text": doc.page_content,
                        "source": doc.metadata.get("source", file_path),
                        "page": doc.metadata.get("page", None),
                        "file_name": file,
                        "path": file_path
                    }
                    for doc in components
                ]

                qdrant_db.insert(
                    ids=ids,
                    vectors=vectors,
                    payloads=payloads
                )

                total_vectors += len(ids)
                total_files += 1

                print(f"Inserted {len(ids)} vectors from {file}")

                checked_files.append(files)

            except Exception as e:
                print(f"Failed ingest {file_path}: {e}")

    print("\n========== INGEST SUMMARY ==========")
    print(f"Files processed: {total_files}")
    print(f"Total vectors inserted: {total_vectors}")