from rest_framework import serializers
from app.models import NudityDetection

class NudityDetectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NudityDetection
        fields = ['id', 'image_url', 'created_at']
        read_only_fields = ['created_at'] 