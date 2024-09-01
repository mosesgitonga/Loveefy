from django.db import models
# from django.contrib.auth.models import User
from .user import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class Preference(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.CharField(max_length=25, null=False, db_index=True)
    min_age = models.IntegerField(default=18, null=True)
    max_age = models.IntegerField(default=65, null=True)
    country = models.CharField(max_length=30, null=True, db_index=True)
    region = models.CharField(max_length=30, null=True)
    industry_major = models.CharField(max_length=50, default='any', null=True, db_index=True)
    career = models.CharField(max_length=36)
    education_level = models.CharField(max_length=40, default='any')
    employment = models.CharField(max_length=20)
    is_schooling = models.CharField(max_length=10)
    fav_hobby = models.CharField(max_length=50)
    wants_child = models.CharField(max_length=25, default='any')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=True, db_index=True)

    def serialize(self):
        return {
            "id": self.id,
            "gender": self.gender,
            "min_age": self.min_age,
            "max_age": self.max_age,
            "country": self.country,
            "region": self.region,
            "industry_major": self.industry_major,
            "career": self.career,
            "education_level": self.education_level,
            "employment": self.employment,
            "is_schooling": self.is_schooling,
            "fav_hobby": self.fav_hobby,
            "wants_child": self.wants_child
        }
