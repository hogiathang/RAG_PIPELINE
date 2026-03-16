from src.common.model.agent_adapter import AgentAdapter
from src.common.model.agent_prompt import AGENT_PROMPT
from transformers import AutoModelForCausalLM, AutoTokenizer
from threading import Lock

MODEL_NAME  = "Qwen/Qwen3-4B-Instruct-2507"
TEMPERATURE = 0.7
MAX_TOKENS  = 2048

class LocalAgent(AgentAdapter):
    _instance = None
    _lock = Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LocalAgent, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.model_name = MODEL_NAME
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, device_map="auto")
        self._initialized = True

    def execute_task(self, prompt, task_type):
        system_instruction = AGENT_PROMPT.get(task_type, "")
        
        messages = [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]

        text_prompt = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = self.tokenizer(
            text_prompt, 
            return_tensors="pt"
        ).to(self.model.device)

        input_length = inputs.input_ids.shape[1]

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_tokens = outputs[0][input_length:]

        result = self.tokenizer.decode(generated_tokens, skip_special_tokens=True)

        return result