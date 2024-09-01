from django.contrib import admin
from .models.user import User
from .models.likes import Likes, Matches
from .models.profile import UserProfile
from .models.place import Place
from .models.preference import Preference
from .models.upload import Upload
from .models.recommendation import Recommendation
from .models.messages import Room, Messages

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