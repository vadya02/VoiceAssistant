# serializers.py
from rest_framework import serializers
from .models import RequestHistory
from django.contrib.auth import get_user_model
class AudioFileSerializer(serializers.Serializer):
    audio_file = serializers.FileField()
class RequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestHistory
        fields = '__all__'


User = get_user_model()