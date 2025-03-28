from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

import requests
import tempfile
import os
import imghdr

from app.models import NudityDetection
from app.tasks import detect_nudity
from app.serializers import NudityDetectionSerializer
from app.permissions import IsOwner


class NudityDetectionView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['App'],
        methods=["POST"],
        description='Nudity Detection',
        responses={200: {"message": "Password changed successfully"}},
    )

    def post(self, request):
        image_url = request.data.get('image_url')
        original_url = image_url

        if not image_url:
            return Response(
                {"error": "image_url is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:

            response = requests.get(image_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(response.content)
                temp_path = temp_file.name
            
            image_type = imghdr.what(temp_path)
            if not image_type:
                # Clean up the temporary file
                os.unlink(temp_path)
                return Response(
                    {"error": "Uploaded file is not a valid image"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Start the Celery task with the temporary file path
            task = detect_nudity.delay(temp_path, request.user.id, original_url)
            
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
            # Clean up the temporary file in case of error
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DetectionResultsListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['App'],
        methods=["GET"],
        description='API view for listing all nudity detection results for the current user',
        responses={200: NudityDetectionSerializer(many=True)},
    )

    def get(self, request):
        detections = NudityDetection.objects.filter(user=request.user)
        serializer = NudityDetectionSerializer(detections, many=True)
        return Response(serializer.data)


class DetectionResultDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    @extend_schema(
        tags=['App'],
        methods=["GET"],
        description='API view for retrieving a specific nudity detection result',
        responses={200: NudityDetectionSerializer()},
    )

    def get(self, request, pk):
        detection = get_object_or_404(
            NudityDetection, 
            pk=pk, 
            user=request.user
        )
        serializer = NudityDetectionSerializer(detection)
        return Response(serializer.data)