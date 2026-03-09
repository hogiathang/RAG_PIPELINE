import json
import re
import requests
from typing import List, Dict

# Giả định bạn đã import GeminiAgent từ src.common.gemini_agent
# from src.common.gemini_agent import GeminiAgent

class WebSearchEngine:
    def __init__(self, serper_api_key: str = None):
        # self.agent = GeminiAgent()
        self.serper_api_key = serper_api_key

    def _gen_gemini_query(self, code: str) -> List[str]:
        """
        Nhận code đầu vào, phân tích và trả về danh sách các search query tối ưu.
        """
        # Giả lập call agent của bạn
        # gemini_response = self.agent.execute_task(
        #     prompt=f"Analyze this code snippet...\n\n{code}",
        #     task_type="code-to-query"
        # )
        
        # Mock response để test logic
        gemini_response = """
        {
            "suspicion_level": "High",
            "identified_behavior": "Executes base64 decoded string via child_process.",
            "extracted_artifacts": ["child_process.exec", "Buffer.from", "base64"],
            "search_queries": [
                "npm package malicious base64 child_process.exec buffer.from",
                "nodejs reverse shell base64 child_process"
            ]
        }
        """

        def validate_response(response: str) -> dict:
            # 1. Làm sạch markdown backticks nếu LLM vẫn cố tình sinh ra
            cleaned = response.strip()
            cleaned = re.sub(r'^```(?:json)?', '', cleaned)
            cleaned = re.sub(r'```$', '', cleaned).strip()

            # 2. Cố gắng parse JSON
            try:
                parsed_data = json.loads(cleaned)
            except json.JSONDecodeError as e:
                raise ValueError(f"Không thể parse JSON từ Gemini response: {e}\nRaw: {response}")

            # 3. Validate các trường bắt buộc theo prompt
            required_keys = ["suspicion_level", "identified_behavior", "extracted_artifacts", "search_queries"]
            for key in required_keys:
                if key not in parsed_data:
                    raise ValueError(f"Missing required key: '{key}' in Gemini output.")

            # 4. Đảm bảo search_queries là một list hợp lệ
            if not isinstance(parsed_data["search_queries"], list) or len(parsed_data["search_queries"]) == 0:
                raise ValueError("'search_queries' phải là một mảng và không được rỗng.")

            return parsed_data

        validated_data = validate_response(gemini_response)
        
        # Có thể log suspicion_level hoặc identified_behavior ra để tracking
        print(f"[THREAT INTEL] Suspicion: {validated_data['suspicion_level']}")
        print(f"[THREAT INTEL] Behavior: {validated_data['identified_behavior']}")

        return validated_data["search_queries"]

    def _perform_web_search(self, queries: List[str]) -> str:
        """
        Thực hiện gọi API Web Search (Ví dụ dùng Serper.dev API)
        """
        if not self.serper_api_key:
            return "WARNING: Chưa cấu hình API Key cho Web Search."

        url = "https://google.serper.dev/search"
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }

        all_results_summary = []

        # Chỉ lấy tối đa 2 query đầu tiên để tránh call API quá nhiều
        for idx, query in enumerate(queries[:2]):
            payload = json.dumps({"q": query, "num": 3}) # Lấy 3 kết quả top đầu mỗi query
            
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 200:
                results = response.json().get("organic", [])
                
                all_results_summary.append(f"--- Results for Query {idx+1}: '{query}' ---")
                for item in results:
                    title = item.get("title", "No Title")
                    snippet = item.get("snippet", "No Snippet")
                    link = item.get("link", "#")
                    all_results_summary.append(f"- {title}\n  Snippet: {snippet}\n  URL: {link}\n")
            else:
                all_results_summary.append(f"[API ERROR] Query '{query}' failed with status {response.status_code}")

        return "\n".join(all_results_summary)

    def search(self, code: str) -> str:
        """
        Hàm chính nhận code đầu vào, thực hiện end-to-end flow
        """
        try:
            print("[INFO] Bắt đầu phân tích code và tạo Search Queries...")
            optimized_queries = self._gen_gemini_query(code)
            
            print(f"[INFO] Đã tạo {len(optimized_queries)} queries. Bắt đầu tìm kiếm...")
            search_results = self._perform_web_search(optimized_queries)
            
            return search_results
        except ValueError as ve:
            print(f"[VALIDATION ERROR] {ve}")
            return "Web search failed do LLM trả về format không hợp lệ."
        except Exception as e:
            print(f"[ERROR] Quá trình tìm kiếm thất bại: {e}")
            return "Web search failed do lỗi hệ thống."