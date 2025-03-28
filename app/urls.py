from django.urls import path
from .views import (
    NudityDetectionView, 
    DetectionResultsListView, 
    DetectionResultDetailView
)

urlpatterns = [
    path('app/detect/', NudityDetectionView.as_view(), name='detect-nudity'),
    path('app/results/', DetectionResultsListView.as_view(), name='detection-results'),
    path('app/results/<int:pk>/', DetectionResultDetailView.as_view(), name='detection-result-detail'),
]