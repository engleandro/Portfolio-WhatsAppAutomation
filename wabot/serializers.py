from rest_framework import serializers
from wabot.models import MessageWABot

class MessageWABotSerializer(serializers.ModelSerializer):
    model = MessageWABot
    fields = [
        "from_phone",
        "to_phone",
        "message"
        ]
