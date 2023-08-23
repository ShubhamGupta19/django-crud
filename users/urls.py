from django.urls import path
from .apis.user_profile import register_user
urlpatterns = [
    path("register/", register_user)
]
