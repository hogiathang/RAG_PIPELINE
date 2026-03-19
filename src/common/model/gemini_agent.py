import os
from queue import Queue, Empty
import concurrent.futures
from threading import Lock
from google.genai import Client, types
from src.common.model.agent_config import AGENT_PROMPT
from uuid import uuid4
from threading import Thread
import time
from src.common.model.agent_adapter import AgentAdapter
from src.logging.log_manager import AppLogger

logger = AppLogger.get_logger(__name__)

MODEL_NAME = "gemini-2.5-flash"
TOKENS_FILE = "api_tokens/gemini_tokens.txt"

# =========================================================
# Lớp Worker bên trong (Được khởi tạo 1 lần duy nhất trên mỗi token)
# =========================================================
class Worker:
    def __init__(self, token, model_name):
        self.token = token
        self.id = str(uuid4())[:8]
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

# -----------------------------------------

class GeminiAgent(AgentAdapter):
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
        self.worker_status = {}
        self.workers = {}

        def prepare_worker(token):
            worker = Worker(token, self.model_name)
            if worker.is_available():
                self.worker_status[worker.id] = "available"
                return worker
            else:
                self.worker_status[worker.id] = "unavailable"
            return None
        
        api_tokens = self._load_tokens(token_file_path)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(api_tokens)) as executor:
            future_to_token = {executor.submit(prepare_worker, token): token for token in api_tokens}
            for future in concurrent.futures.as_completed(future_to_token):
                worker = future.result()
                if worker:
                    self.worker_pool.put(worker)
                    self.workers[worker.id] = worker
                
        self._initialized = True

        recovery_thread = Thread(target=self._worker_recovery_loop, daemon=True)
        recovery_thread.start()

    def _worker_recovery_loop(self):
        while True:
            try:
                self.check_and_invoke_worker()
            except Exception as e:
                logger.error("Worker recovery loop error: %s", e)

            time.sleep(60)

    def _load_tokens(self, token_file_path) -> list:
        tokens = []
        if not os.path.exists(token_file_path):
            logger.error(f"Token file '{token_file_path}' not found. Please create the file and add your API tokens, one per line.")
            return tokens
        else:
            with open(token_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    token = line.strip()
                    if token:
                        tokens.append(token)
        return tokens
    
    def check_and_invoke_worker(self):
        """
        Ping các worker đang bị đánh dấu là 'unavailable'.
        Nếu worker hoạt động trở lại thì đưa vào pool.
        """

        recovered = []

        for worker_id, status in list(self.worker_status.items()):

            if status != "unavailable":
                continue

            worker = self.workers.get(worker_id)

            if worker is None:
                continue

            try:
                if worker.is_available():
                    self.worker_status[worker_id] = "available"
                    self.worker_pool.put(worker)
                    recovered.append(worker_id)

            except Exception:
                continue

        if recovered:
            logger.info(f"[INFO] Recovered Gemini Workers: {', '.join(recovered)}")
        else:
            logger.info("[INFO] No Gemini Workers recovered in this cycle.")

    def execute_task(self, prompt, task_type="summary-generation"):
        """
        Giao việc cho Worker rảnh. Khóa worker trong lúc xử lý và trả lại pool sau khi xong.
        Param:
            - prompt: Nội dung công việc cần thực hiện (ví dụ: code snippet để phân tích)
            - task_type: Loại công việc để chọn system prompt phù hợp:
                + "code-to-query": Phân tích code và tạo search query
                + "summary-generation": Tổng hợp thông tin và tạo báo cáo phân tích
        """
        if task_type not in AGENT_PROMPT:
            logger.error(f"Invalid task type '{task_type}'. Please choose from: {', '.join(AGENT_PROMPT.keys())}")
            return None

        while True:
            try:
                worker: Worker = self.worker_pool.get(timeout=60)

                if self.worker_status.get(worker.id) != "available":
                    logger.info(f"[INFO] Worker {worker.id} is currently unavailable. Skipping...")
                    continue

                system_prompt  = AGENT_PROMPT.get(task_type, "")

                result = worker.perform_task(prompt, system_instruction=system_prompt)

                if result is None:
                    self.worker_status[worker.id] = "unavailable"
                    logger.error(f"[ERROR] Worker {worker.id} failed to perform task. Marking as unavailable.")
                    continue

                self.worker_pool.put(worker)
                return result
            
            except Empty:
                print("[ERROR] No Gemini Worker available. All workers are busy or failed to initialize.")
                return None
            
            except Exception as e:
                self.worker_status[worker.id] = "unavailable"
                logger.error(f"[ERROR] Worker {worker.id} encountered an error: {str(e)}. Marking as unavailable.")
                continue