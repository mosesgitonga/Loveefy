from django.db import models
# from django.contrib.auth.models import User
from .user import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class UserProfile(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=20, null=False)
    DOB = models.DateTimeField(null=False)
    mobile_no = models.CharField(max_length=16, unique=True, null=False, db_index=True)
    education_level = models.CharField(max_length=36, blank=True)
    industry_major = models.CharField(max_length=25, null=False)
    employment = models.CharField(max_length=25, blank=True)
    is_schooling = models.CharField(max_length=25, blank=True)
    career = models.CharField(max_length=50, null=True, blank=True)
    has_child = models.CharField(max_length=10, default='no')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=True, db_index=True)    
