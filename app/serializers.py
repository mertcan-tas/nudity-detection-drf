from rest_framework import serializers
from app.models import Detection, DetectionResult
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'email')

class DetectionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectionResult
        fields = ('id', 'score', 'raw_result', 'created_at')
        read_only_fields = ('created_at',)

class DetectionSerializer(serializers.ModelSerializer):
    result = DetectionResultSerializer(read_only=True)
    
    class Meta:
        model = Detection
        fields = ('id', 'image_url', 'status', 'created_at', 'result')
        read_only_fields = ('status', 'created_at') 