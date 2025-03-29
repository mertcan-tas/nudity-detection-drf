from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from celery.result import AsyncResult
from app.models import Detection
from app.serializers import DetectionSerializer


class TaskStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=['Detection'],
        methods=["GET"],
        description='Check task status and get result if completed',
        responses={200: DetectionSerializer()},
    )
    def get(self, request, task_id):
        # Get the detection record
        detection = get_object_or_404(Detection, task_id=task_id, user=request.user)
        
        # Check Celery task status
        task_result = AsyncResult(task_id)
        
        response_data = {
            "task_id": task_id,
            "status": detection.status,
            "celery_status": task_result.status
        }
        
        # If task is completed, include the result
        if detection.status == 'completed' and hasattr(detection, 'result'):
            response_data["result"] = {
                "score": detection.result.score,
                "raw_result": detection.result.raw_result
            }
        # If task failed, include the error
        elif detection.status == 'failed':
            response_data["error"] = task_result.result.get('error', 'Unknown error')
            
        return Response(response_data)
