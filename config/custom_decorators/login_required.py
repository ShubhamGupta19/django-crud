from datetime import datetime
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

# from config.helper_functions import validate_email
from config.request_param_validators import get_request_body

from error_handling.custom_exceptions.common_exceptions import RequestBodyValidation

from users.models import UserProfile



def login_required(view_function):
    """Validates the authorization token passed in the headers of the request and
    adds corresponding User and UserProfile instances in the request."""

    def view(request, *original_args, **original_kwargs):
        
        user = None
        if request.method == "OPTIONS":
            pass
        token = request.META.get("HTTP_AUTHORIZATION")
        if get_user_model().objects.filter(username=token).exists():
            user = get_user_model().objects.get(username=token)
        else:
            user = get_user_model().objects.create( username=token, email=get_request_body(request).get("email"))
        print(user)
        print("\nn\n\n\n\n\n\n\n\n")
        if user:
            request.user = user
            try:
                request.user_profile = UserProfile.objects.get(user=user)
            except ObjectDoesNotExist:
                request.user_profile = None
        else:
            request.user = None
            request.user_profile = None
        print("passed")
        return view_function(request, *original_args, **original_kwargs)
    print("passed")
    return view

# def login_required(view_function):
#     """Validates the authorization token passed in the headers of the request and
#     adds corresponding User and UserProfile instances in the request."""

#     def view(request, *original_args, **original_kwargs):
        
#         if request.method == "OPTIONS":
#             pass
#         if request

#     return view