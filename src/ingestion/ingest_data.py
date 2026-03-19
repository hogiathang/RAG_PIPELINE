import os
import uuid
import json
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from tqdm import tqdm

from langchain_community.document_loaders import PyPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

# Giả định các module này đã có sẵn
from RAG_PIPELINE.src.common.model.embedding_model import EmbeddingModel
from RAG_PIPELINE.src.ingestion.qdrant_adapter import QdrantAdapter

# Cấu hình logging
logging.basicConfig(level=logging.ERROR) # Giảm log để tránh làm chậm console
logger = logging.getLogger(__name__)

# Cấu hình hệ thống
INPUT_DIR = "./backup_rag"
CHECKER_FILE = "./checker.json"
MAX_WORKERS = 8  # Tùy thuộc vào số nhân CPU và giới hạn API của bạn
BATCH_SIZE = 100 # Số lượng vector gửi lên Qdrant mỗi lần (nếu file quá lớn)

# Khóa để bảo vệ việc ghi vào file checker
checker_lock = threading.Lock()

def load_checker() -> set:
    if not os.path.exists(CHECKER_FILE):
        return set()
    try:
        with open(CHECKER_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return set(data.get("checks", []))
    except Exception:
        return set()

def update_checker_safe(file_path: str):
    with checker_lock:
        current_data = load_checker()
        current_data.add(file_path)
        try:
            with open(CHECKER_FILE, "w", encoding="utf-8") as f:
                json.dump({"checks": list(current_data)}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger.error(f"Cannot update checker for {file_path}: {e}")

def load_document(file_path: str):
    try:
        suffix = Path(file_path).suffix.lower()
        if suffix == ".pdf":
            return PyPDFLoader(file_path).load()
        elif suffix == ".txt":
            return TextLoader(file_path, encoding="utf-8").load()
        elif suffix == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Document(page_content=json.dumps(data, ensure_ascii=False), metadata={"source": file_path})]
        return None
    except Exception as e:
        logger.error(f"Failed to load document {file_path}: {e}")
        return None

def process_single_file(file_path_obj, qdrant_db, embedding_model, text_splitter):
    file_path = str(file_path_obj)
    
    try:
        documents = load_document(file_path)
        if not documents:
            return 0, file_path

        chunks = text_splitter.split_documents(documents)
        if not chunks:
            return 0, file_path

        texts = [doc.page_content for doc in chunks]
        
        vectors = embedding_model.embed(texts)
        
        if hasattr(vectors, "tolist"): vectors = vectors.tolist()
        if isinstance(vectors, list) and len(vectors) > 0 and isinstance(vectors[0], (int, float)):
            vectors = [vectors]
        
        ids = [str(uuid.uuid4()) for _ in texts]
        payloads = [
            {
                "text": doc.page_content,
                "source": doc.metadata.get("source", file_path),
                "file_name": file_path_obj.name
            }
            for doc in chunks
        ]

        qdrant_db.insert(ids=ids, vectors=vectors, payloads=payloads)
        
        update_checker_safe(file_path)
        
        return len(ids), file_path

    except Exception as e:
        logger.error(f"Error processing file {file_path}: {e}")
        return -1, file_path

def ingest_data():
    qdrant_db = QdrantAdapter()
    embedding_model = EmbeddingModel()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    
    processed_files = load_checker()
    
    all_files = [
        f for f in Path(INPUT_DIR).rglob('*') 
        if f.is_file() and str(f) not in processed_files
    ]
    
    if not all_files:
        print("No new files to process. All files in the input directory have been ingested.")
        return

    print(f"Found {len(all_files)} new files to process.")
    
    total_vectors = 0
    success_count = 0
    
    # Sử dụng ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Gửi tất cả task vào pool
        futures = {
            executor.submit(process_single_file, f, qdrant_db, embedding_model, text_splitter): f 
            for f in all_files
        }
        
        # Hiển thị thanh tiến trình
        for future in tqdm(as_completed(futures), total=len(all_files), desc="Ingesting"):
            vec_count, f_path = future.result()
            if vec_count >= 0:
                total_vectors += vec_count
                success_count += 1

    print(f"Ingestion completed: {success_count}/{len(all_files)} files processed successfully, total vectors inserted: {total_vectors}.")