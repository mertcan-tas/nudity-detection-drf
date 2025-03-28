from celery import shared_task
from app.models import NudityDetection
from django.contrib.auth import get_user_model
from decouple import config
from nudenet import NudeDetector
import os
import cv2
import numpy as np


@shared_task
def detect_nudity(image_path: str, user_id: int, original_url: str):
    try:
        # Read the image using OpenCV
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Failed to read image")
            
        # Initialize NudeDetector
        detector = NudeDetector()
        
        # Perform detection
        result = detector.detect(image_path)

        NUDITY_THRESHOLD=config('NUDITY_THRESHOLD') 

        is_nude = False
        
        # Clean up the temporary file
        os.unlink(image_path)
        
        user = get_user_model().objects.get(id=user_id)
        
        # Calculate score from result
        if result:
            score = max(detection['score'] for detection in result)
        else:
            score = 0.0
            
        # Save the result
        NudityDetection.objects.create(
            user=user,
            score=score
        )
        
        return {
            "success": True,
            "result": result
        }
    
    except Exception as e:
        # Clean up the temporary file in case of error
        if os.path.exists(image_path):
            os.unlink(image_path)
        return {
            "success": False,
            "error": str(e)
        } 