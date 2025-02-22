from rest_framework.response import Response
from rest_framework import generics
from .models import UserPreference, Itinerary
from .serializers import UserPreferenceSerializer, ItinerarySerializer
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from .services.chatbot import ChatbotService

# Instantiate the ChatbotService class
chatbot_service = ChatbotService()

class UserPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

class ItineraryListCreateView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

class ChatbotView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('user-input')
        result = chatbot_service.chat_with_mistral(user_input)
        return Response({"response": result})