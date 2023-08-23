from platform import platform
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from config.request_param_validators import get_request_body
from error_handling.backend.helper_functions import get_api_code
from error_handling.models import FrontendErrors

from error_handling.custom_exceptions.common_exceptions import RequestBodyValidation


@csrf_exempt
@require_http_methods(["POST"])
def log_error(request):
    """logs frontend error in the database

    Args:
        request (object): wsgi request object

    Raises:
        RequestBodyValidation: if api_code, error_description, error_type or platform is not provided

    Returns:
        JSON: a json object with success as true.
    """
    request_body = get_request_body(request)

    api_url = request_body.get("api_url")
    error_description = request_body.get("error_description")
    error_type = request_body.get("error_type")
    platform = request_body.get("platform")
    priority = request_body.get("priority", "default")
    auth_token = request_body.get("auth_token")
    screen = request_body.get("screen")
    app = request_body.get("app")

    request.META["HTTP_AUTHORIZATION"] = auth_token

    if None in (api_url, error_description, error_type, platform):
        raise RequestBodyValidation(
            message="api_url, error_description, error_type and platform are required"
        )

    if platform not in ["android", "ios"]:
        raise RequestBodyValidation(message="platform can only be android or ios")

    if priority not in ["default", "low", "medium", "high"]:
        raise RequestBodyValidation(
            message="priority can only be default, low, medium or high"
        )

    api_code = get_api_code(api_url)

    if auth_token:
        try:
            request = get_user_details(request)
        except Exception:
            request.user_profile = None
    else:
        request.user_profile = None

    FrontendErrors.objects.create(
        api_code=api_code,
        error_description=error_description,
        error_type=error_type,
        platform=platform,
        priority=priority,
        user_profile=request.user_profile,
        screen=screen,
        app=app,
    )

    return JsonResponse({"success": True})


def get_user_details(request):
    return request
