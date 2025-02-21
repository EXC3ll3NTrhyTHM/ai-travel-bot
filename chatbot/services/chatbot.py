from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch

class ChatbotService:
    tokenizer = None
    model = None
    
    def __init__(self):

        # model_name = "microsoft/DialoGPT-medium"
        # 7 billion parameter model. Maybe you could replace with deepseek-ai/DeepSeek-R1 which is a 685B param model 
        # but downloading this model would require better internet than I have and probably like a whole 1tb of space
        # (this mistral model is 32gb), also a better GPU than I have and possibly still multiple GPUs. 
        # mistral model is sufficient.
        model_name = "mistralai/Mistral-7B-Instruct-v0.1"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # or torch.bfloat16 if preferred
            bnb_4bit_use_double_quant=False,
            bnb_4bit_quant_type="nf4"  # or "fp4" depending on your needs
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            quantization_config=quantization_config
        )


    def chat_with_mistral(self, user_input):

        # response = self.model(user_input)
        print(f"User: {user_input}")
        
        prompt = f"User: {user_input}\nTravelBot:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        output = self.model.generate(
            **inputs, 
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            do_sample=True,
            temperature=0.7,
            top_p=0.92,
        )
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        bot_response = response.split("TravelBot:")[-1].strip()

        
        return bot_response