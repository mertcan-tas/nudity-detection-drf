from django.db import models
from django.contrib.auth import get_user_model

class NudityDetection(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Detection for {self.user.email} - Score: {self.score}"

class DetectionResult(models.Model):
    detection = models.ForeignKey(NudityDetection, on_delete=models.CASCADE, related_name='result')
    score = models.FloatField()
    url = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result for {self.detection.user.email} - Score: {self.score}"
