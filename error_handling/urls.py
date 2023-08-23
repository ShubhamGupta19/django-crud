from django.urls import path
from error_handling.apis.frontend_errors import log_error

urlpatterns = [
    path("log-error", log_error),
]
