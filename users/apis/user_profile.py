from datetime import date, datetime
from enum import unique
import os
from platform import platform
import random
import string

from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from  django.core.validators import validate_email
from config.custom_decorators.login_required import login_required
from config.request_param_validators import get_request_body
from error_handling.custom_exceptions.common_exceptions import RequestBodyValidation
from error_handling.custom_exceptions.frontend_exceptions import UnknownAppVersion

from users.models import  UserProfile

from django.db.models import F



@csrf_exempt
@login_required
@require_http_methods(["POST"])
def register_user(request):
    """Register the user or update if already registered

    Args:
        request (object): wsgi request object

    Returns:
        [JsonReponse]: Data for all user attributes
    """
    
    request_body = get_request_body(request)
    
    if None in [
        request_body.get("email"),
        request_body.get("first_name"),
        request_body.get("last_name"),
    ]:
        raise RequestBodyValidation(
            message="email, first_name, last_name are required"
        )
    
    email = request_body.get("email")
    first_name = request_body.get("first_name")
    last_name = request_body.get("last_name")
    
    try:
        validate_email(email)
    except Exception:
        raise RequestBodyValidation(message="email is not valid")
    
    user_profile, created = UserProfile.objects.get_or_create(
        email=email,
        defaults={
            "first_name": first_name,
            "last_name": last_name,
        },
        user = request.user
    )
    
    if not created:
        user_profile.first_name = first_name
        user_profile.last_name = last_name
        user_profile.save()
    
    return JsonResponse(user_profile.to_dict())

