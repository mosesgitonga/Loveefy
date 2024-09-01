from django.db import models
# from django.contrib.auth.models import User
from .user import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class Upload(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    image_path = models.CharField(max_length=200, unique=True, null=False, db_index=True)
    created_at = models.DateTimeField(null=False, default=timezone.now)
    is_primary = models.BooleanField(default=False)
    file_size = models.CharField(max_length=12, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=True, db_index=True)

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "image_path": self.image_path,
            "is_primary": self.is_primary,
            "file_size": self.file_size
        }