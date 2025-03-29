from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.utils import timezone
from datetime import timedelta

import requests
import tempfile
import os
import imghdr

from .models import Detection, DetectionResult
from .tasks import detect_nudity
from .serializers import DetectionSerializer
from .permissions import IsOwner




class NudityDetectionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Detection'],
        methods=["POST"],
        description='Start a new nudity detection',
        responses={202: {"task_id": str, "message": str}},
    )
    def post(self, request):
        image_url = request.data.get('image_url')
        
        if not image_url:
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Download the image
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Create detection record
            detection = Detection.objects.create(
                user=request.user,
                image_url=image_url
            )
            
            # Save image temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            # Validate image
            image_type = imghdr.what(temp_path)
            if not image_type:
                os.unlink(temp_path)
                detection.status = 'failed'
                detection.save()
                return Response(
                    {"error": "Invalid image file"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Start the Celery task
            task = detect_nudity.delay(temp_path, detection.id)
            detection.task_id = task.id
            detection.save()
            
            return Response({
                "task_id": task.id,
                "message": "Detection started"
            }, status=status.HTTP_202_ACCEPTED)
            
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Failed to download image: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DetectionResultsListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Detection'],
        methods=["GET"],
        description='List all detections for the current user',
        responses={200: DetectionSerializer(many=True)},
    )
    def get(self, request):
        detections = Detection.objects.filter(user=request.user)
        serializer = DetectionSerializer(detections, many=True)
        return Response(serializer.data)


class DetectionResultDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @extend_schema(
        tags=['Detection'],
        methods=["GET"],
        description='Get details of a specific detection',
        responses={200: DetectionSerializer()},
    )
    def get(self, request, pk):
        detection = get_object_or_404(Detection, pk=pk, user=request.user)
        serializer = DetectionSerializer(detection)
        return Response(serializer.data)