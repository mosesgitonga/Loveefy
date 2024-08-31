from django.contrib import admin
from .models import User, Likes, UserProfile, Place, Preference, Upload, Matches, Recommendation, Room, Messages

admin.site.register(User)
admin.site.register(Likes)
admin.site.register(UserProfile)
admin.site.register(Place)
admin.site.register(Preference)
admin.site.register(Upload)
admin.site.register(Matches)
admin.site.register(Recommendation)
admin.site.register(Room)
admin.site.register(Messages)