import uuid
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from shots.models import Shot

class Feedback(models.Model):
    feedback_uuid = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    user = models.ForeignKey(get_user_model(), related_name='feedbacks', on_delete=models.CASCADE)
    shot = models.ForeignKey(Shot, related_name='feedbacks', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created', )
    
