from django.urls import path

from . import views

# Your api routes go here
urlpatterns = [
    path("moses/", views.moses),
]