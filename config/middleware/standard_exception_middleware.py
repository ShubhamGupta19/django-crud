from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from config.request_param_validators import get_request_body

from error_handling.backend.helper_functions import (
    get_debug_log,
    get_error_code,
    get_error_object,
    log_error,
)
from users.models import UserProfile


class StandardExceptionMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        """This method is triggered when an exception is raised from an API or middleware

        Args:
            request (object): A WSGIRequest object. The request sent by the API call
            exception (object): An exception object. The exception raised by the API

        Returns:
            [JsonResponse]: The error JSON
        """

        error_code = get_error_code(request.path, request.method, exception)
        debug_log = get_debug_log(exception)
        error = get_error_object(error_code=error_code)
        user_message = error.user_message if error else None
        request_body = get_request_body(request)
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except Exception as e:
            print("The error occured in process_exception:", e, e.__class__.__name__)
            user_profile = None

        if (error and not error.ignore) or (error is None):
            log_error(exception, error_code, user_profile, debug_log, request_body)

        return JsonResponse(
            {
                "error_code": error_code,
                "debug_log": debug_log,
                "user_message": user_message,
            }
        )
