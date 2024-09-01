from django.db import models
# from django.contrib.auth.models import User
from .user import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='recommended_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='recommended_user_2')
    score = models.IntegerField(db_index=True)
    def serialize(self):
        return {
            "recommendations": self.id,
            "user_1": self.user_1.id,
            "user_2": self.user_2.id,
            "score": self.score
        }