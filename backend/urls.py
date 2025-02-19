from django.contrib import admin
from django.urls import path
from chatbot.views import UserPreferenceListCreateView, ItineraryListCreateView, search_hotels_by_city, search_flights

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user-preferences/', UserPreferenceListCreateView.as_view(), name='user-preferences'),
    path('api/itineraries/', ItineraryListCreateView.as_view(), name='itineraries'),
    path('api/search-flights/', search_flights, name='search-flights'),
    path('api/search-hotels/', search_hotels_by_city, name='search-hotels'),
]
