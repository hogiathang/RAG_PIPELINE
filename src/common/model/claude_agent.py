import os
import json
import time
from threading import Lock
from anthropic import Anthropic, APIError, APIStatusError, APITimeoutError
from src.common.model.agent_adapter import AgentAdapter
from src.common.model.agent_config import AGENT_PROMPT
from src.logging.log_manager import AppLogger

logger = AppLogger.get_logger(__name__)

# Cấu hình chiến lược Retry
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5  # Giây nghỉ giữa các lần thử lại
MODEL_MAPPING = {
    "skills-analysis": "claude-haiku-4-5-20251001",
    "skills-report-generation": "claude-sonnet-4-6"
}

class ClaudeAgent(AgentAdapter):
    _instance = None
    _lock = Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ClaudeAgent, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        self._initialized = True
        self.client = self._load_client()

    def _load_client(self):
        claude_key = os.environ.get("CLAUDE_API_KEY", "")
        if not claude_key:
            raise ValueError("CLAUDE_API_KEY environment variable is not set.")

        return Anthropic(api_key=claude_key, timeout=300.0)

    def _get_tool_definition(self):
        """Định nghĩa Tool chung để nhận kết quả JSON"""
        return {
            "name": "submit_result",
            "description": "Output the final analysis or report in strict JSON format.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "output": {
                        "type": "object",
                        "description": "The actual JSON data of the task."
                    }
                },
                "required": ["output"]
            }
        }

    def execute_task(self, prompt, task_type) -> str:
        """Thực thi task với cơ chế Retry và Safe Fallback"""
        selected_model = MODEL_MAPPING.get(task_type, "claude-sonnet-4-6")
        
        for attempt in range(MAX_RETRIES):
            try:
                logger.info(f"Executing {task_type} (Model: {selected_model}) - Attempt {attempt + 1}/{MAX_RETRIES}")
                
                response = self.client.messages.create(
                    model=selected_model,
                    max_tokens=8192,
                    temperature=0,
                    system=[{
                        "type": "text",
                        "text": AGENT_PROMPT.get(task_type, ""),
                        "cache_control": {"type": "ephemeral"}
                    }],
                    tools=[self._get_tool_definition()],
                    tool_choice={"type": "tool", "name": "submit_result"},
                    messages=[{"role": "user", "content": prompt}]
                )

                for block in response.content:
                    if block.type == "tool_use":
                        result_data = block.input.get("output", block.input)
                        return json.dumps(result_data, ensure_ascii=False)
                
                if response.content:
                    return response.content[0].text

            except (APITimeoutError, APIStatusError, APIError) as e:
                logger.warning(f"Claude API Error (Attempt {attempt + 1}): {e}")
                if attempt < MAX_RETRIES - 1:
                    sleep_time = RETRY_DELAY_SECONDS * (attempt + 1)
                    logger.info(f"Sleeping for {sleep_time} seconds before retry...")
                    time.sleep(sleep_time)
                else:
                    logger.error(f"Max retries reached for {task_type}. Failing gracefully.")
            
            except Exception as e:
                logger.error(f"Unexpected error in ClaudeAgent: {e}")
                break # Lỗi logic code thì không nên retry

        return "{}"