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

class Room(models.Model):
    id = models.CharField(max_length=75, primary_key=True)
    name = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    members = models.ManyToManyField(User)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name, 
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'members': [member.serialize() for member in self.members]
        }

class Messages(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    content = models.CharField(max_length=1024, null=False)
    time = models.DateTimeField(auto_now_add=True, null=False)
    status = models.CharField(max_length=20, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, db_index=True, related_name='receiver')


