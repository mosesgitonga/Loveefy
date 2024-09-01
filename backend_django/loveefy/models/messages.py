from django.db import models
# from django.contrib.auth.models import User
from .user import User

import uuid
from datetime import datetime, timedelta
from django.utils import timezone
from enum import Enum

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


