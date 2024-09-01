from django.db import models
# from django.contrib.auth.models import User
from .user import User
import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

class Place(models.Model):
    id = models.CharField(max_length=120, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    country = models.CharField(max_length=150, null=False, db_index=True)
    region = models.CharField(max_length=100, null=False, db_index=True)
    sub_region = models.CharField(max_length=100, null=False)
    longitude = models.IntegerField(null=True)
    latitude = models.IntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, unique=True, db_index=True)

    def serialize(self):
        return {
            "id": self.id,
            "country": self.country,
            "region": self.region,
            "sub_region": self.sub_region,
            "longitude": self.longitude,
            "latitude": self.latitude
        }    


