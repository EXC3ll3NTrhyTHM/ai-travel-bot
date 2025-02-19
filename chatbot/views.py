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

def get_amadeus_access_token():
    """
    Function to get an access token from the Amadeus API.

    This function:
    - Tries to retrieve the access token from the cache.
    - If not found, requests a new access token from the Amadeus API.
    - Caches the access token for future use.
    - Returns the access token.   
    
    """
    # Try to get the access token from cache
    access_token = cache.get("amadeus_access_token")
    if access_token:
        print("Access token retrieved from cache")
        return access_token

    # Access environment variables loaded in settings.py
    client_id = settings.AMADEUS_API_KEY
    client_secret = settings.AMADEUS_API_SECRET
    token_request_url = settings.AMADEUS_TOKEN_URL

    # Request an access token from Amadeus (using the test endpoint)
    token_response = requests.post(
        token_request_url,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    # Throw error if unable to fetch access token
    if token_response.status_code != 200:
        return  Response({"error": "Unable to fetch access token from Amadeus"}, status=token_response.status_code)
    
    # Retrieve access token and expiration time
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    expires_in = token_data.get('expires_in', 3600)  # seconds

    # Cache the access token for future use
    if access_token:
        cache.set("amadeus_access_token", access_token, timeout=expires_in-60)

    return token_response.json().get('access_token')

@api_view(['GET'])
def search_flights(request):
    """
    Endpoint to search for flight offers from the Amadeus API.
    
    This function:
    - Retrieves the necessary query parameters from the request.
    - Obtains an access token either from the cache or by requesting a new one.
    - Calls the Amadeus flight search endpoint using the provided parameters.
    - Returns a JSON response with flight offers or an error message.

    """
    access_token = get_amadeus_access_token()
    amadeus_api_v2_root_url = settings.AMADEUS_API_V2_ROOT_URL
    
    # Build parameters for flight search
    params = {
        "originLocationCode": request.GET.get('originLocationCode'),
        "destinationLocationCode": request.GET.get('destinationLocationCode'),
        "departureDate": request.GET.get('departureDate'),
        "adults": request.GET.get('adults', 1)  # defaults to 1 adult if not specified
    }

    # Call the Amadeus flight search endpoint
    flight_response = requests.get(
        amadeus_api_v2_root_url + "shopping/flight-offers",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=params
    )

    # Throw error if unable to fetch flight offers
    if flight_response.status_code != 200:
        return Response({"error": "Error fetching flight offers", "details": flight_response.json()}, status=flight_response.status_code)

    return Response(flight_response.json())

@api_view(['GET'])
def search_hotels_by_city(request):
    """
    Endpoint to search for hotels in a city using the Amadeus API.
    
    This function:
    - Retrieves the necessary query parameters from the request.
    - Obtains an access token either from the cache or by requesting a new one.
    - Calls the Amadeus hotel search endpoint using the provided parameters.
    - Returns a JSON response with hotel offers or an error message
    
    """
    access_token = get_amadeus_access_token()
    amadeus_api_v1_root_url = settings.AMADEUS_API_V1_ROOT_URL
    
    # Build parameters for hotel search
    params = {
        "cityCode": request.GET.get('cityCode'),
        'radius': request.GET.get('radius', 5),  # defaults to 5km if not specified
    }

    # Call the Amadeus hotel search endpoint
    hotel_response = requests.get(
        amadeus_api_v1_root_url + "reference-data/locations/hotels/by-city",
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=params
    )

    # Throw error if unable to fetch hotel offers
    if hotel_response.status_code != 200:
        return Response({"error": "Error fetching hotel offers", "details": hotel_response.json()}, status=hotel_response.status_code)

    return Response(hotel_response.json())

@api_view(['GET'])
def search_hotels_by_geo(request):
    """
    Endpoint to search for hotels in a city using the Amadeus API.
    
    This function:
    - Retrieves the necessary query parameters from the request.
    - Obtains an access token either from the cache or by requesting a new one.
    - Calls the Amadeus hotel search endpoint using the provided parameters.
    - Returns a JSON response with hotel offers or an error message
    
    """
    access_token = get_amadeus_access_token()
    amadeus_api_v1_root_url = settings.AMADEUS_API_V1_ROOT_URL
    
    # Build parameters for hotel search
    params = {
        "latitude": request.GET.get('latitude'),
        'longitude': request.GET.get('longitude'),
        'radius': request.GET.get('radius', 5),  # defaults to 5km if not specified
        'ratings': request.GET.get('ratings', '4')  # defaults to 4 and 5 star hotels if not specified
    }

    api_url = amadeus_api_v1_root_url + "reference-data/locations/hotels/by-geocode"
    print(api_url)

    # Call the Amadeus hotel search endpoint
    hotel_response = requests.get(
        api_url,
        headers={
            "Authorization": f"Bearer {access_token}"
        },
        params=params
    )

    # Throw error if unable to fetch hotel offers
    if hotel_response.status_code != 200:
        return Response({"error": "Error fetching hotel by geo offers", "details": hotel_response.json()}, status=hotel_response.status_code)

    return Response(hotel_response.json())