from rest_framework import generics
from .models import UserPreference, Itinerary
from .serializers import UserPreferenceSerializer, ItinerarySerializer
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.cache import cache


class UserPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

class ItineraryListCreateView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

