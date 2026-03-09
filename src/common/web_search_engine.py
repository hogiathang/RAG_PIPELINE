from src.common.gemini_agent import GeminiAgent
import json, re, os
import requests
from threading import Lock
from typing import List

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

    def validate_response(self, response: str) -> dict:
            if not response:
                raise ValueError("Empty response from Gemini Agent.")
            
            cleaned = response.strip()
            cleaned = re.sub(r'^```(?:json)?', '', cleaned)
            cleaned = re.sub(r'```$', '', cleaned).strip()

            try:
                parsed_data = json.loads(cleaned)
            except json.JSONDecodeError as e:
                raise ValueError(f"Can not parse JSON from Gemini response: {e}\nRaw: {response}")

            required_keys = ["suspicion_level", "identified_behavior", "extracted_artifacts", "search_queries"]

            for key in required_keys:
                if key not in parsed_data:
                    raise ValueError(f"Missing required key: '{key}' in Gemini output.")

            if not parsed_data["search_queries"]:
                parsed_data["search_queries"] = [f"No search query found for the provided snippet"] 
            
            return parsed_data

    def _analyze_code_with_agent(self, code: str) -> dict:
        print(f"[INFO] Task type: {self.task_type}")
        gemini_response = self.agent.execute_task(
            prompt=f"Analyze this code snippet and generate an optimized search query to find relevant information:\n\n{code}",
            task_type=self.task_type
        )

        return self.validate_response(gemini_response)

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
        
    def analyze_code_and_search_web(self, source_code: str) -> list[str]:
        """
        Analyze source code to generate optimized search queries,
        execute web searches, and aggregate enriched threat intelligence results.
        """
        try:
            analysis_result = self._analyze_code_with_agent(source_code)
            print(f"[INFO] Gemini analysis result: {analysis_result}")
            generated_queries = analysis_result.get("search_queries", [])

            print(f"[INFO] Generated search queries: {generated_queries}")
            aggregated_search_output = []

            for query in generated_queries:
                print(f"[INFO] Executing web search for query: '{query}'")
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

            aggregated_search_output.extend(
                analysis_result.get("identified_behavior", [])
            )
            aggregated_search_output.extend(
                analysis_result.get("extracted_artifacts", [])
            )

            return aggregated_search_output

        except Exception as error:
            print(f"[ERROR] Web search execution failed: {error}")
            return ["Web search execution failed due to an error."]


if __name__ == "__main__":
    js_code_slice = """
    const fs = require('fs');
    const { exec } = require('child_process');

    function handleFileUpload(file) {
        const filePath = `/tmp/${file.name}`;
        fs.writeFileSync(filePath, file.data);
        exec(`python3 process_file.py ${filePath}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error processing file: ${error}`);
                return;
            }
            console.log(`File processed successfully: ${stdout}`);
        });
    }
    """

    search_engine = WebSearchEngine()
    results = search_engine.analyze_code_and_search_web(js_code_slice)
    print(results)