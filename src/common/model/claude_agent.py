from src.common.model.agent_adapter import AgentAdapter
from src.common.model.agent_config import AGENT_PROMPT
from threading import Lock
from src.logging.log_manager import AppLogger
from anthropic import Anthropic, types
import os

MODEL_NAME= "claude-haiku-4-5-20251001"

SUPPORTED_MODEL=[
    "claude-opus-4-6",
    "claude-opus-4-5-20251101",
    "claude-opus-4-1-20250805",
    "claude-opus-4-20250514",
    "claude-sonnet-4-6",
    "claude-sonnet-4-5-20250929",
    "claude-sonnet-4-20250514",
    "claude-haiku-4-5-20251001"
]

logger = AppLogger.get_logger(__name__)

class ClaudeAgent(AgentAdapter):
    _instance = None
    _lock = Lock()
    
    def __new__(cls, *args, **kwargs):
        """Đảm bảo GeminiAgent là Singleton (Thread-safe)"""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ClaudeAgent, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.model = self._load_model()
        self.model_name = MODEL_NAME

    def _load_model(self):
        claude_key = os.environ.get("CLAUDE_API_KEY", "")

        if not claude_key:
            logger.error("Claude API key is not configured. Please set the CLAUDE_API_KEY environment variable.")
            raise ValueError("Claude API key is not configured.")

        return Anthropic(api_key=claude_key)

    def execute_task(self, prompt, task_type) -> str:
        try:
            response = self.model.messages.create(
                model=self.model_name,
                system=AGENT_PROMPT.get(task_type, ""),
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=4096,
                temperature=0.2
            )

            return response.content[0].text

        except Exception as e:
            logger.error(f"Error executing task with ClaudeAgent: {e}")
            return None


