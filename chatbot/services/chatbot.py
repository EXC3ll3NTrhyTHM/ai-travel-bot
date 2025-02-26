from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import time
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.memory.chat_message_histories import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage


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
        {chat_history}

        Human: {input} 
        AI: [/INST]"""

        # template = """<s>[INST] First if the human does not ask about traveling then just respond politely. If they do ask about traveling answer the question by first giving a conversational answer. Next extract the important entities from the generated response and place them in the travel object. Extract all locations, then extract all airports, then extract specific activities and finally extract the dates.

        #     Desired format of travel object:
        #     [travel-obj]
        #     Locations: <comma_separated_list_of_locations>
        #     Airports: <comma_separated_list_of_airports>
        #     Activities: <comma_separated_list_of_activities>
        #     Dates: <comma_separated_list_of_dates>
        #     [/travel-obj]

        #     {chat_history}

        #     Human: {input}[/INST]

        # """


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
            pad_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=512,
            temperature=0.6,
            top_p=0.9,
            do_sample=True,
        )

        llm = HuggingFacePipeline(pipeline=pipe)

        message_history = ChatMessageHistory()

        self.memory = ConversationBufferMemory(
             memory_key="chat_history", 
             chat_memory=message_history,
             return_messages=True)

        prompt = PromptTemplate(input_variables=["chat_history", "input"], template=template)
        
        self.conversation = ConversationChain(
            llm=llm,
            memory=self.memory,
            prompt=prompt,
            verbose=True
        )

    def chat_with_mistral(self, user_input):
        response = self.conversation.predict(input=user_input)
        bot_response = response.split("[/INST]")[-1].strip()

        def generate_response():
            for token in bot_response.split():
                yield token + " "
                time.sleep(0.1)  # Simulating streaming delay

        # self.memory.chat_memory.add_user_message(user_input)
        # self.memory.chat_memory.add_ai_message(bot_response)

        print(bot_response)

        return StreamingHttpResponse(generate_response(), content_type="text/plain")