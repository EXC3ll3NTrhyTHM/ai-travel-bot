import uuid
from django.db import models
from langchain.memory import ConversationBufferMemory

class UserPreference(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    budget = models.FloatField(null=True, blank=True)
    preferred_locations = models.JSONField(default=list)  # Store list of destinations
    interests = models.JSONField(default=list)  # ["Food", "Luxury", "History"]

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    memory_data = models.TextField(default='[]')  # Serialized memory
    
    def get_memory(self):
        """Deserialize and return LangChain memory object"""
        memory = ConversationBufferMemory()
        if self.memory_data:
            # Implement deserialization logic based on how you store memory
            # This is just a placeholder
            import json
            memory_dict = json.loads(self.memory_data)
            # Reconstruct memory from dictionary
        return memory
    
    def save_memory(self, memory):
        """Serialize and save memory object"""
        # Implement serialization logic
        # This is just a placeholder
        import json
        memory_dict = {
            "buffer": memory.buffer,
            # Add other memory attributes as needed
        }
        self.memory_data = json.dumps(memory_dict)
        self.save()

class Itinerary(models.Model):
    user = models.ForeignKey(UserPreference, on_delete=models.CASCADE)
    details = models.JSONField(default=dict)  # Store trip details
    total_cost = models.FloatField()
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)

    def add_chat_entry(self, user_input, bot_response):
        # Logic to update the itinerary based on chat
        pass