import json
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig
)
from config import MODEL_NAME, MAX_TOKENS, TEMPERATURE
from agent.prompt import build_prompt

from vision.vision_commands import *
from vision.vision_controller import VisionController
from vision.vision_context import build_vision_context



vision = VisionController()



PERSONA_CONFIG = {
    "default": {
        "system_prompt": "You are a friendly AI assistant.",
        "voice": "en"
    },
    "teacher": {
        "system_prompt": "You explain things step by step.",
        "voice": "en"
    },
    "arabic_friend": {
        "system_prompt": "You speak Arabic casually and friendly.",
        "voice": "ar"
    }
}



class AssistantAgent:
    def __init__(self, personality_file, memory,persona="default"):
        self.tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            use_fast=True
            
        )

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True
            
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            torch_dtype=torch.float16,
            quantization_config=bnb_config,
            device_map="cuda"
        )

        with open(personality_file, "r", encoding="utf-8") as f:
            self.personality = json.load(f)
            
        self.memory = memory
        
        self.persona = persona
        
        self.voice_lang = PERSONA_CONFIG[self.persona]["voice"]
        
        self.personality.setdefault(
            "system_prompt",
            PERSONA_CONFIG[self.persona]["system_prompt"]
        )

    def respond(self, user_input: str) -> str:
        vision_context = ""
        if is_open_camera_cmd( user_input):
            return vision.open_camera()

        if is_describe_cmd( user_input):
             vision.describe()
             vision_context = build_vision_context() 
         
        if is_close_camera_cmd( user_input):
            return vision.close_camera()
                  # not a vision command
                  
              
        prompt = build_prompt(
            self.personality["system_prompt"] + vision_context,
            self.memory.get(),
            user_input
        )

        inputs = self.tokenizer(prompt, return_tensors="pt").to("cuda")

        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )

        response = self.tokenizer.decode(
            output[0],
            skip_special_tokens=True
        )
        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        response = decoded.split("<|im_start|>assistant")[-1].strip()
        self.memory.add(user_input, response)

        return response[response.rindex("assistant")+9:-1]
