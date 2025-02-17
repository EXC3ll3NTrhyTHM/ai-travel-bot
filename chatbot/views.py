from rest_framework import generics
from .models import UserPreference, Itinerary
from .serializers import UserPreferenceSerializer, ItinerarySerializer
import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

class UserPreferenceListCreateView(generics.ListCreateAPIView):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

class ItineraryListCreateView(generics.ListCreateAPIView):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer

@api_view(['GET'])
def search_flights(request):
        # Access environment variables loaded in settings.py
    client_id = settings.AMADEUS_API_KEY
    client_secret = settings.AMADEUS_API_SECRET

    # Request an access token from Amadeus (using the test endpoint)
    token_response = requests.post(
        "https://test.api.amadeus.com/v1/security/oauth2/token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    if token_response.status_code != 200:
        return Response({"error": "Unable to fetch access token from Amadeus"}, status=token_response.status_code)

    access_token = token_response.json().get('access_token')
    if not access_token:
        return Response({"error": "Access token not found in response"}, status=500)
    
    print(request.GET)

    # Build parameters for flight search
    params = {
        "originLocationCode": request.GET.get('originLocationCode'),
        "destinationLocationCode": request.GET.get('destinationLocationCode'),
        "departureDate": request.GET.get('departureDate'),
        "adults": request.GET.get('adults', 1)  # defaults to 1 adult if not specified
    }

    # Call the Amadeus flight search endpoint
    flight_response = requests.get(
        "https://test.api.amadeus.com/v2/shopping/flight-offers",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=params
    )

    if flight_response.status_code != 200:
        return Response({"error": "Error fetching flight offers", "details": flight_response.json()}, status=flight_response.status_code)

    return Response(flight_response.json())

# @api_view(['GET'])
# def search_hotels(request):
#     response = requests.get("https://api.expedia.com/v3/hotels", params={'city': request.GET.get('city')})
#     return Response(response.json())