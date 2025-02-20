from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class ChatbotService:
    tokenizer = None
    model = None
    
    def __init__(self):

        model_name = "microsoft/DialoGPT-medium"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto"
        )


    def chat_with_mistral(self, user_input):

        # response = self.model(user_input)
        print(f"User: {user_input}")
        
        prompt = f"User: {user_input}\nTravelBot:"
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        output = self.model.generate(**inputs, max_length=1000,pad_token_id=self.tokenizer.eos_token_id,do_sample=True,temperature=0.7)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        return response