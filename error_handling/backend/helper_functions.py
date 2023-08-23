import traceback

from django.core.exceptions import ObjectDoesNotExist

from error_handling.models import Api, ApiMethodCall, ErrorList, ErrorLogs, ErrorName


def get_api_code(path):
    """Returns the first two paramter of error code

    Args:
        path (str): The url of the API

    Returns:
        [str]: The first two parameter of error code
    """

    try:
        api = Api.objects.get(url=path[path.find("/api") :])
        return api.section.code + "." + api.code
    except ObjectDoesNotExist:
        try:
            api = Api.objects.get(
                url=path[path.find("/whiprides") : path.rfind("/") + 1]
            )
            return api.section.code + "." + api.code
        except Exception as e:
            # this print statement is to help when an error occurs while error handling
            print("The error occured in get_api_code:", e, e.__class__.__name__)
            return "00"


def get_method_code(method):
    """Returns the method code corresponding to the inpur string. This is required to generate
    the error code for the exception occurred in the API call.

    Args:
        method (str): The method call of the API

    Returns:
        [str]: The code corresponding to the method call.
    """

    try:
        return ApiMethodCall.objects.get(method=method).code
    except Exception as e:
        # this print statement is to help when an error occurs while error handling
        print(
            "The error occured in get_method_code:",
            e,
            e.__class__.__name__,
            "The method passed was",
            method,
        )
        return "O"


def get_error_and_specific_codes(exception):
    """Returns the last two paramter of error code

    Args:
        exception (object): The exception occurred during the API call

    Returns:
        [str]: The last two parameter of error code
    """

    try:
        error_code = ErrorName.objects.get(name=exception.__class__.__name__).code
    except ObjectDoesNotExist:
        try:
            if exception.__cause__:
                error_code = ErrorName.objects.get(
                    name=exception.__cause__.__class__.__name__
                ).code
            else:
                error_code = "00"
        except ObjectDoesNotExist:
            error_code = "00"
        except Exception as e:
            # this print statement is to help when an error occurs while error handling
            print(
                "The error occured in get_error_and_specific_codes:",
                e,
                e.__class__.__name__,
            )
            error_code = "-"
    except Exception as e:
        # this print statement is to help when an error occurs while error handling
        print(
            "The error occured in get_error_and_specific_codes:",
            e,
            e.__class__.__name__,
        )
        error_code = "-"

    if error_code == "00":
        try:
            specific_code = exception.specific_code
        except AttributeError:
            specific_code = "00"
    else:
        specific_code = "00"

    return error_code + "." + specific_code


def get_error_code(path, method, exception):
    """Returns the complete error code.

    Args:
        path (str): The path of the API call
        method (str): The method call of the API
        exception (object): The exception that occurredn during the API call

    Returns:
        [str]: The complete error code
    """

    api_code = get_api_code(path)
    method_code = get_method_code(method)
    error_code = get_error_and_specific_codes(exception)

    return ".".join([api_code, method_code, error_code])


def get_debug_log(exception):
    """The traceback to the point where the exception occurred

    Args:
        exception (object): The exception that occurred during the API call

    Returns:
        [str]: The complete traceback of the exception
    """

    try:
        log = exception.__class__.__name__ + ": " + str(exception)
        log += "\n" + "".join(
            traceback.format_list(traceback.extract_tb(exception.__traceback__))
        )
        return log
    except Exception as e:
        # this print statement is to help when an error occurs while error handling
        print("The error occured in get_debug_log:", e, e.__class__.__name__)
        return ""


def get_error_object(error_code):
    try:
        return ErrorList.objects.get(error_code=error_code)
    except ObjectDoesNotExist:
        return None
    except Exception as e:
        # this print statement is to help when an error occurs while error handling
        print(
            "The error occured in get_error_details_from_table:",
            e,
            e.__class__.__name__,
        )
        return None


def get_extra_debug_information(exception):
    try:
        return exception.extra_information
    except AttributeError:
        return None
    except Exception as e:
        # this print statement is to help when an error occurs while error handling
        print(
            "The error occured in get_extra_debug_information:", e, e.__class__.__name__
        )
        return None


def log_error(
    exception, error_code, user_profile=None, debug_log=None, request_body=None
):
    if debug_log is None:
        debug_log = get_debug_log(exception)

    ErrorLogs.objects.create(
        user_profile=user_profile,
        error_code=error_code,
        debug_log=debug_log,
        request_body=request_body,
        extra_debug_information=get_extra_debug_information(exception),
    )
