from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import time
from rest_framework.response import Response
from django.http import StreamingHttpResponse

class ChatbotService:
    tokenizer = None
    model = None
    chat_history = ""
    
    def __init__(self):
        # model_name = "microsoft/DialoGPT-medium"
        model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        # model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        # model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
        self.initialize_model(model_name)

        
    def initialize_model(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # or torch.bfloat16 if preferred
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",  # or "fp4" depending on your needs
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            quantization_config=quantization_config,
        )

        self.chat_history = ""
        
    def chat_with_mistral(self, user_input):
        if self.chat_history:
            prompt = f"{self.chat_history}\nUser: {user_input}\nTravelBot:"
        else:
            prompt = f"User: {user_input}\nTravelBot:"

        print(prompt)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # Stream responses
        def generate_response():
            outputs = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=100,
                temperature=0.6,
                top_p=0.95,
                do_sample=True,
                return_dict_in_generate=True
            )

            decoded_text = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
            bot_response = decoded_text.split("TravelBot:")[-1].strip()

            for token in bot_response.split():
                yield token + " "
                time.sleep(0.1)  # Simulating streaming delay

        return StreamingHttpResponse(generate_response(), content_type="text/plain")
