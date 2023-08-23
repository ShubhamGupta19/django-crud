from django.core.exceptions import PermissionDenied


class RequestBodyValidation(Exception):
    default_message = "The request body passed is invalid."
    default_code = "request_body_invalid"

    def __init__(self, specific_code=None, extra_information=None, message=None):
        self.specific_code = "01" if specific_code is None else specific_code
        self.extra_information = extra_information
        self.message = message

    def __str__(self):
        return self.default_message if self.message is None else self.message


class UserAccessDenied(PermissionDenied):
    default_message = "The user does not have access to %s."
    default_code = "user_access_denied"

    def __init__(self, access_denied_to, specific_code=None, extra_information=None):
        self.specific_code = "02" if specific_code is None else specific_code
        self.default_message = self.default_message % access_denied_to
        self.extra_information = extra_information

    def __str__(self):
        return self.default_message

