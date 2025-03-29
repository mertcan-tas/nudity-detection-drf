from django.urls import path
from .views import (
    NudityDetectionView, 
    DetectionResultsListView, 
    DetectionResultDetailView,

)

urlpatterns = [

    path('detect/', NudityDetectionView.as_view(), name='detect-nudity'),
    path('results/', DetectionResultsListView.as_view(), name='detection-results'),
    path('results/<int:pk>/', DetectionResultDetailView.as_view(), name='detection-result-detail'),
]