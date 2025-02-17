from django.db import models

class UserPreference(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    budget = models.FloatField(null=True, blank=True)
    preferred_locations = models.JSONField(default=list)  # Store list of destinations
    interests = models.JSONField(default=list)  # ["Food", "Luxury", "History"]

class Itinerary(models.Model):
    user = models.ForeignKey(UserPreference, on_delete=models.CASCADE)
    details = models.JSONField(default=dict)  # Store trip details
    total_cost = models.FloatField()