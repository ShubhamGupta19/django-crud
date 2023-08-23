class UnknownAppVersion(Exception):
    default_message = "Unknown app version"
    default_code = "unknown_app_version"

    def __init__(self, specific_code=None, extra_information=None, message=None):
        self.specific_code = "41" if specific_code is None else specific_code
        self.extra_information = extra_information
        self.message = message

    def __str__(self):
        return self.default_message if self.message is None else self.message


class ActiveAppVersionDoesNotExist(Exception):
    default_message = "Active app version does not exist"
    default_code = "active_app_version_does_not_exist"

    def __init__(self, specific_code=None, extra_information=None, message=None):
        self.specific_code = "42" if specific_code is None else specific_code
        self.extra_information = extra_information
        self.message = message

    def __str__(self):
        return self.default_message if self.message is None else self.message
