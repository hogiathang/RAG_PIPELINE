from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from src.generation.model_config import ModelConfig
from src.generation.prompt import Prompt
import torch

# base_model_id = "deepseek-ai/deepseek-coder-6.7b-instruct"
base_model_id = "Qwen/Qwen2.5-Coder-0.5B-Instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True
)

# Load model & tokenizer
# "deepseek-ai/deepseek-coder-6.7b-instruct"
class AIModel:
    def __init__(self, config : ModelConfig):
        self.config = config

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_id,
            trust_remote_code=True,
            use_fast=False
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_id,
            device_map="auto",
            trust_remote_code=True,
            quantization_config=bnb_config,
        )
    def read_file(self, file_path : Path):
        # Nếu file_path là relative, resolve dựa trên folder model.py
        if not file_path.exists() and not file_path.is_absolute():
            file_path = Path(__file__).parent / file_path
            if not file_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read().strip()

    def tokenize(self, code : str): 
        # Read prompts from given file
        prompt = [
            {"role": "system", "content": self.read_file(Path("system-prompt.txt"))},
            {"role": "user", "content": code}
        ]
        inputs = self.tokenizer.apply_chat_template(
            prompt,
            add_generation_prompt=True,
            return_tensors="pt",
            return_dict=True
        )
        # inputs = inputs.to(self.model.device)

        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        return inputs
    # def build_instruction_prompt(self, instruction: str):
    #     return f'''
    # You are a professional static security code auditor.  

    # Your task: analyze a single JavaScript (or Node.js) code fragment (a "code slice") and output EXACTLY one JSON object only.  

    # STRICT RULES:
    # 1. Do NOT execute the code. Perform only static analysis.
    # 2. ALWAYS return exactly one JSON object. 
    # 3. DO NOT add explanations, comments, or extra text.  
    # 4. DO NOT wrap JSON in markdown or quotes.  
    # 5. If unsure, use 0.0 for numeric fields.
    # 6. Follow the exact key order below:

    # {{
    # "confidence": float,
    # "obfuscated": float,
    # "malware": float,
    # "securityRisk": float
    # }}

    # ### Instruction:
    # {instruction.strip()}

    # ### Response:
    # '''.lstrip()
    # def tokenize(self, input_file_path: Path):
    # # Read JS / code slice (instruction)
    #     instruction = self.read_file(input_file_path)

    #     # Build prompt EXACTLY like SFT training
    #     prompt_text = self.build_instruction_prompt(instruction)

    #     # Tokenize (NO chat template)
    #     inputs = self.tokenizer(
    #         prompt_text,
    #         return_tensors="pt",
    #         truncation=True,
    #         max_length=self.tokenizer.model_max_length,
    #     )

    #     # Ensure PAD token consistency
    #     if self.tokenizer.pad_token_id is None:
    #         self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

    #     # Move tensors to model device
    #     inputs = inputs.to(self.model.device)

    #     return inputs
    def generate(self, inputs) -> str:
        # Generate output
        input_ids = inputs["input_ids"]

        with torch.no_grad():
            outputs = self.model.generate(
                # input_ids=inputs,
                **inputs,
                # attention_mask=(inputs != self.tokenizer.pad_token_id),
                max_new_tokens=self.config.max_new_tokens,
                do_sample=self.config.do_sample,
                top_k=self.config.top_k,
                top_p=self.config.top_p,
                temperature=self.config.temperature,
                num_return_sequences=self.config.num_return_sequences,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        # Decode only generated tokens
        return self.tokenizer.decode(
            # outputs[0][inputs.shape[1]:],
            outputs[0][input_ids.shape[1]:],
            skip_special_tokens=True
        )
        
    def generate_batch(self, prompts : list[Prompt]) -> list[str]:
        self.tokenizer.padding_side = "left"

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id

        formatted_prompts = [
            self.tokenizer.apply_chat_template(
                prompt, 
                tokenize=False, 
                add_generation_prompt=True
            )
            for prompt in prompts
        ]

        inputs = self.tokenizer(
            formatted_prompts,
            return_tensors="pt",
            padding=True,
            padding_side="left",
            truncation=True
        ).to(self.model.device)

        with torch.no_grad(), torch.autocast(device_type=self.model.device.type, dtype=torch.float16):
            outputs = self.model.generate(
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=self.config.max_new_tokens,
                do_sample=self.config.do_sample,
                top_k=self.config.top_k,
                top_p=self.config.top_p,
                temperature=self.config.temperature,
                num_return_sequences=1, # Batching thì nên chỉ trả về 1 sequence mỗi prompt
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        input_length = inputs.input_ids.shape[1]

        generated_tokens = outputs[:, input_length:]

        decoded_responses = self.tokenizer.batch_decode(
            generated_tokens, 
            skip_special_tokens=True
        )

        return decoded_responses