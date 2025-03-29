from celery import shared_task
from .models import Detection, DetectionResult
from django.contrib.auth import get_user_model
from decouple import config
from nudenet import NudeDetector
import os
import cv2
import numpy as np


@shared_task
def detect_nudity(image_path: str, detection_id: int):
    try:
        detection = Detection.objects.get(id=detection_id)
        detection.status = 'processing'
        detection.save()

        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to read image")
            
        # Initialize NudeDetector
        detector = NudeDetector()
        
        # Perform detection
        result = detector.detect(image_path)
        
        # Clean up the temporary file
        os.unlink(image_path)
        
        # Calculate score from result
        if result:
            score = max(detection['score'] for detection in result)
        else:
            score = 0.0
            
        # Create the result
        DetectionResult.objects.create(
            detection=detection,
            score=score,
            raw_result=result
        )
        
        detection.status = 'completed'
        detection.save()
        
        return {
            "success": True,
            "result": result
        }
    
    except Exception as e:
        # Update detection status to failed
        if 'detection' in locals():
            detection.status = 'failed'
            detection.save()
            
        # Clean up the temporary file in case of error
        if os.path.exists(image_path):
            os.unlink(image_path)
        return {
            "success": False,
            "error": str(e)
        } 