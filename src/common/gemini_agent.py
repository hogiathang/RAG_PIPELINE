import os
from queue import Queue, Empty
import concurrent.futures
from threading import Lock
from google.genai import Client, types
from src.common.agent_config import AGENT_PROMPT, MODEL_NAME, TOKENS_FILE
# -----------------------------------------

class GeminiAgent:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        """Đảm bảo GeminiAgent là Singleton (Thread-safe)"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(GeminiAgent, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_name=MODEL_NAME, token_file_path=TOKENS_FILE):
        if self._initialized:
            return
            
        self.model_name = model_name
        self.worker_pool = Queue()

        def prepare_worker(token):
            worker = self.Worker(token, self.model_name)
            if worker.is_available():
                return worker
            return None
        
        api_tokens = self._load_tokens(token_file_path)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(api_tokens)) as executor:
            future_to_token = {executor.submit(prepare_worker, token): token for token in api_tokens}
            for future in concurrent.futures.as_completed(future_to_token):
                worker = future.result()
                if worker:
                    self.worker_pool.put(worker)

                
        self._initialized = True
        print(f"[INFO] GeminiAgent is available with {self.worker_pool.qsize()} workers ready.")

    def _load_tokens(self, token_file_path) -> list:
        tokens = []
        if not os.path.exists(token_file_path):
            print(f"[WARNING] Token file '{token_file_path}' not found. No workers will be available.")
            return tokens

        with open(token_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                token = line.strip()
                if token:
                    tokens.append(token)
        return tokens

    def execute_task(self, prompt, task_type="summary-generation"):
        """
        Giao việc cho Worker rảnh. Khóa worker trong lúc xử lý và trả lại pool sau khi xong.
        Param:
            - prompt: Nội dung công việc cần thực hiện (ví dụ: code snippet để phân tích)
            - task_type: Loại công việc để chọn system prompt phù hợp:
                + "code-to-query": Phân tích code và tạo search query
                + "summary-generation": Tổng hợp thông tin và tạo báo cáo phân tích
        """
        try:
            worker = self.worker_pool.get(timeout=60)
        except Empty:
            return None

        try:
            system_prompt = AGENT_PROMPT.get(task_type, "")
            return worker.perform_task(prompt, system_instruction=system_prompt)
        finally:
            self.worker_pool.put(worker)
            self.worker_pool.task_done()

    # =========================================================
    # Lớp Worker bên trong (Được khởi tạo 1 lần duy nhất trên mỗi token)
    # =========================================================
    class Worker:
        def __init__(self, token, model_name):
            self.token = token
            self.masked_token = f"{token[:8]}...{token[-4:]}" # Che token để log an toàn
            self.model_name = model_name
            self.client = Client(api_key=token)

        def is_available(self):
            try:
                self.client.models.generate_content(
                    model=self.model_name,
                    contents="ping"
                )
                return True
            except Exception as e:
                return False

        def perform_task(self, prompt, system_instruction=None):
            try:
                config = types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.2 
                )
                
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                return None

if __name__ == "__main__":
    # Bước 1: Gọi Agent (Lúc này nó sẽ load token và dựng Worker Pool)
    agent = GeminiAgent()
    
    # Bước 2: Dù khởi tạo lại ở hàm khác, nó vẫn trỏ về instance cũ nhờ Singleton
    another_agent_reference = GeminiAgent()
    assert agent is another_agent_reference 

    print("\n[INFO] GeminiAgent đã được khởi tạo và sẵn sàng sử dụng.\n")
    
    # Bước 3: Gửi code slice vào để phân tích
    js_code_slice = "eval(Buffer.from('Y29uc29sZS5sb2coInB3bmVkIik=', 'base64').toString());"
    
    result = agent.execute_task(
        prompt=f"Analyze this suspicious Node.js slice:\n\n{js_code_slice}",
        task_type="code-to-query"
    )
    
    print("\n[RESULT]:\n", result)