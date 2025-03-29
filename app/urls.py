from django.urls import path

from app.views import NudityDetectionView, DetectionResultsListView, DetectionResultDetailView, TaskStatusView

urlpatterns = [
    path('detect/', NudityDetectionView.as_view(), name='detect-nudity'),
    path('results/', DetectionResultsListView.as_view(), name='detection-results'),
    path('results/<int:pk>/', DetectionResultDetailView.as_view(), name='detection-result-detail'),
    path('task/<str:task_id>/', TaskStatusView.as_view(), name='task-status'),
]