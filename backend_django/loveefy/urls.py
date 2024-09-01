from django.urls import path
from .views.auth import moses

urlpatterns = [
    path("moses/", moses),
]
