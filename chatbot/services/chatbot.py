from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import time
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate


class ChatbotService:
    tokenizer = None
    model = None
    chat_history = ""
    
    def __init__(self):
        # model_name = "microsoft/DialoGPT-medium"
        # model_name = "mistralai/Mistral-7B-Instruct-v0.2"
        # model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
        # model_name = "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B"
        model_name = "mistralai/Mistral-7B-Instruct-v0.3"
        self.initialize_model(model_name)

        
    def initialize_model(self, model_name):

        template = """<s>[INST] Give one answer and only generate the AI's response. Do not include the Human's input or the AI's name in the response.
        
        Current conversation:
        {chat_history}
        Human: {input}
        AI: [/INST]"""


        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # or torch.bfloat16 if preferred
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",  # or "fp4" depending on your needs
            llm_int8_enable_fp32_cpu_offload=True
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype="auto",
            device_map="auto",
            quantization_config=quantization_config,
        )

        pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            max_new_tokens=512,
            temperature=0.6,
            top_p=0.9,
            # Add other parameters as needed
        )

        llm = HuggingFacePipeline(pipeline=pipe)

        self.memory = ConversationBufferMemory(
             memory_key="chat_history", 
             return_messages=True)
        
        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)

        
        conversation = ConversationChain(
            llm=llm,
            memory=self.memory,
            prompt=prompt,
            verbose=True
        )

        response = conversation.predict(input="Hello, how are you?")
        print(response)
        
    def chat_with_mistral(self, user_input):
        systemPrompt = "You are a travel assistant. Please be concise and don't repeat yourself."
        if self.chat_history:
            prompt = f"{systemPrompt}\n\n{self.chat_history}\nUser: {user_input}\nTravelBot:"
        else:
            prompt = f"{systemPrompt}\n\nUser: {user_input}\nTravelBot:"

        print(prompt)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        print(inputs)

        return StreamingHttpResponse(self.generate_response(inputs, user_input), content_type="text/plain")
    
    def generate_response(self, inputs, user_input):
            outputs = self.model.generate(
                inputs.input_ids,
                attention_mask=inputs.attention_mask,
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=1000,
                return_dict_in_generate=True
            )

            decoded_text = self.tokenizer.decode(outputs.sequences[0], skip_special_tokens=True)
            bot_response = decoded_text.split("TravelBot:")[-1].strip()

            for token in bot_response.split():
                yield token + " "
                time.sleep(0.1)  # Simulating streaming delay

            # self.chat_history += f"\nUser: {user_input}\nTravelBot: {bot_response}"
            print(self.chat_history)