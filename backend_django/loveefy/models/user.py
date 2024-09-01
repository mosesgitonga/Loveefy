from django.db import models
# from django.contrib.auth.models import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class User(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=40, null=False, unique=True,  db_index=True)
    password = models.CharField(max_length=150, null=False)
    username = models.CharField(max_length=80, unique=True, null=True, db_index=True)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
        }
