from django.urls import path

from .apis.user_profile import health_check

urlpatterns = [
    path("health-check/", health_check),
]
