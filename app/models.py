from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Detection(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')  # pending, processing, completed, failed
    task_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Detection for {self.user.email}"

class DetectionResult(models.Model):
    detection = models.OneToOneField(Detection, on_delete=models.CASCADE, related_name='result')
    score = models.FloatField()
    raw_result = models.JSONField()  # Store the complete NudeNet result
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Result for detection {self.detection.id} - Score: {self.score}"
