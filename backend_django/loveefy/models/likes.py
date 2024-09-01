from django.db import models
# from django.contrib.auth.models import User
from .user import User

import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class Likes(models.Model):
    id = models.CharField(max_length=36, default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(default=timezone.now)
    user_who_liked = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='likes_given', db_index=True)
    user_who_was_liked = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='likes_received', db_index=True)

class Matches(models.Model):
    STATUS_CHOICES = [
    ('matched', 'Matched'),
    ('pending', 'Pending'),
    ('declined', 'Declined'),
]
    
    id = models.CharField(max_length=36, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=36, choices=STATUS_CHOICES, default='pending')
    user_1 = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='matched_user_1')
    user_2 = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='matched_user_2')
