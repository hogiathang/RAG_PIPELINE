from src.common.model.gemini_agent import GeminiAgent
from threading import Lock
import os, re, json, requests

TOKENS_FILE = "api_tokens/search_engine_api_keys.txt"

class WebSearchEngine:

    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(WebSearchEngine, cls).__new__(cls)
                cls._instance._initialized = False
        
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.agent = GeminiAgent()
        self.num_response = 1
        self.search_api_keys = self._load_tokens(TOKENS_FILE)
        self.search_engine_url = "https://api.tavily.com/search"
        self._initialized = True
        self.task_type = "skills-to-query"

    def _load_tokens(self, token_file_path) -> list:
        tokens = []
        if not os.path.exists(token_file_path):
            return tokens

        with open(token_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                token = line.strip()
                if token:
                    tokens.append(token)
        return tokens

    def _execute_web_search(self, query: str) -> dict:

        if not self.search_api_keys:
            raise ValueError("Search API key is not configured.")
        
        if not hasattr(self, "current_key_index"):
            self.current_key_index = 0

        attempts = 0

        while attempts < len(self.search_api_keys):
            current_key = self.search_api_keys[self.current_key_index]

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {current_key}"
            }
        
            payload = {
                "query": query,
                "search_depth": "basic",
                "topic": "general",         
                "max_results": getattr(self, "num_response", 1),
                "include_answer": True      
            }

            try:
                response = requests.post(self.search_engine_url, 
                                         headers=headers, 
                                         json=payload, 
                                         timeout=15)

                if response.status_code == 200:
                    return response.json()

                error_details = "Unknown error"

                try:
                    error_json = response.json()
                    error_details = error_json.get("error", response.text)
                except Exception:
                    error_details = response.text

                status = response.status_code

                if status == 400:
                    print(f"[ERROR] Bad request for query '{query}': {error_details}")
                    return {"results": []}
                
                elif status in [401, 429, 432, 433]:
                    self.current_key_index = (self.current_key_index + 1) % len(self.search_api_keys)

                    attempts += 1
                    continue
                else:
                    print(f"[ERROR] Network error for query '{query}': {error_details}")
                    return {"results": []}
                
            except requests.exceptions.RequestException as e:
                print(f"[ERROR] Exception during web search for query '{query}': {e}")
                return {"results": []}
        
    def search(self, query: str) -> list[str]:
        """
        Analyze source code to generate optimized search queries,
        execute web searches, and aggregate enriched threat intelligence results.
        """
        try:
            aggregated_search_output = []

            web_response = self._execute_web_search(query)
            search_hits = web_response.get("results", [])
            print(f"[INFO] Web search hits for query '{query}': {search_hits}")

            for hit in search_hits:
                url = hit.get("url")
                title = hit.get("title")
                content = hit.get("content")
                relevance_score = hit.get("score")

                aggregated_search_output.append(
                    f"URL: {url}\n"
                    f"Title: {title}\n"
                    f"Content: {content}\n"
                    f"Score: {relevance_score}\n\n"
                )

            return aggregated_search_output

        except Exception as error:
            print(f"[ERROR] Web search execution failed: {error}")
            return ["Web search execution failed due to an error."]