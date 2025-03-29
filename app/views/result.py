from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from app.paginations import CustomCursorPagination

from app.models import Detection
from app.serializers import DetectionSerializer
from app.permissions import IsOwner

class DetectionResultsListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = CustomCursorPagination

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