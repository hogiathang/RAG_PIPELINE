"""
test_rag_pipeline.py
────────────────────
Security test cases for the RAG pipeline.

Architecture under test
───────────────────────
  src.retrieval.retrieval
      build_query_prompt(code)          → str
      retrieve_similar_documents(q)     → List[str]   (calls QdrantAdapter)

  src.common.qdrant_adapter
      QdrantAdapter.search(q, top_k)    → List[str]   (calls _search + TODO web)
      QdrantAdapter._search(q, top_k)   → dict{contexts, sources}

External dependencies mocked
─────────────────────────────
  qdrant_client.QdrantClient            – vector database
  sentence_transformers.SentenceTransformer – embedding model

The tests do NOT modify any production source file.
"""