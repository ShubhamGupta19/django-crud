import sys
import traceback
from django.db import models
from django_mysql.models.fields.enum import EnumField

from users.models import UserProfile


class ApiMethodCall(models.Model):
    """Mapping each method call to a code

    method: name of the method call, for example GET, POST, PUT, etc
        The values in the column must be in upper case only
    code: code assigned to each method
    """

    method = models.CharField(max_length=20, unique=True, db_index=True)
    code = models.CharField(max_length=5, unique=True)
    alias = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        db_table = "m_error_api_method_call"


class ErrorName(models.Model):
    """Mapping each error to a code

    name: name of the error, for example ObjectDoesNotExists, ValueError, etc
        The values in the column must be in camel case only
    code: code assigned to each error
    """

    name = models.CharField(max_length=20, unique=True, db_index=True)
    code = models.CharField(max_length=5, unique=True)
    alias = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        db_table = "m_error_name"


class ApiSection(models.Model):
    """Mapping each api section to a code

    name: name of the api section, for example UserProfile, Aid, etc
        The values in the column must be in camel case only
    code: code assigned to each api section
    """

    name = models.CharField(max_length=20, unique=True, db_index=True)
    code = models.CharField(max_length=5, unique=True)
    alias = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        db_table = "m_error_api_section"


class Api(models.Model):
    """Mapping each api to a code

    name: name of the api
    code: code assigned to each api
    url: url of the api
        The url must start from '/api'
    section: the section to which the api belongs to
        FK to ApiSection model
    """

    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=5)
    url = models.URLField(unique=True, db_index=True, max_length=500)
    section = models.ForeignKey(ApiSection, on_delete=models.CASCADE)
    alias = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        db_table = "m_error_api"
        unique_together = ["code", "section"]


class ErrorList(models.Model):
    """Define all the error and its details

    error_code: code of the particular error
        It should follow the code logic -
        'Api Section Code'.'Api Code'.'Method Call Code'.'Error Name Code'.'Defined Number'
    user_message: message to be shown on the frontend
    ignore: if true, the corresponding error should not get logged
    priority: the priority given to the error, (Enum 'default', 'low', 'medium', 'high')
        The value defaults to 'default'
    error_type: the type of the error, (Enum 'default','error','warning','information')
        The value defaults to 'default'
    documentation: a field to maintain the documentation related to the error
    """

    error_code = models.CharField(max_length=15, unique=True, null=False)
    user_message = models.TextField(null=True)
    ignore = models.BooleanField()
    priority = EnumField(
        choices=["default", "low", "medium", "high"], default="default"
    )
    error_type = EnumField(
        choices=["default", "error", "warning", "information"], default="default"
    )
    documentation = models.TextField()
    alias = models.CharField(max_length=255, null=True, unique=True)

    class Meta:
        db_table = "m_error_list"


class ErrorLogs(models.Model):
    """Log of errors that occur while using the app

    user_profile: user who faced the error
    error_code: code of the particular error
        It should follow the code logic -
        'Api Section Code'.'Api Code'.'Method Call Code'.'Error Name Code'.'Defined Number'
    debug_log: the system traceback for when the error occured
    request_body: the body sent to the api
    extra_debug_information: any further informatin required to debug the error
    entry_date: occurence date and time of the error
    device_info: information of the device
    origin_ip: the ip of the origin
    resolved_status: if true, then the error is resolved
        The value defaults to false
    """

    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    error_code = models.CharField(max_length=200, null=True)
    debug_log = models.TextField(null=True)
    request_body = models.JSONField(null=True)
    extra_debug_information = models.JSONField(null=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    device_info = models.CharField(max_length=200, null=True)
    origin_ip = models.CharField(max_length=100, null=True)
    resolved = models.BooleanField(default=0)

    class Meta:
        db_table = "error_log"

    def log_error(
        user_profile,
        request_body,
        error_id,
        exception=None,
        priority="default",
        error_type="default",
        message="",
    ):
        """Enters the error log in the error_logs table and returns a dict to display"""

        system_info = sys.exc_info()
        # uncomment the below line when the only place this function is called is in custom decorator
        # message = str(system_info[1])
        trace = traceback.extract_tb(system_info[2])

        if exception:
            # creating the debug_log output
            debug_log = "ERROR IN THE SERVER: %s" % (exception)
            debug_log += " TRACEBACK is: "
            for (file, linenumber, affected, line) in trace:
                debug_log += "  > ERROR AT FUNCTION %s  " % (affected)
                debug_log += "  >  AT LINE NUMBER : %s:%s" % (file, linenumber)
                debug_log += "  >  SOURCE : %s " % (line)
        else:
            debug_log = ""

        # adding the error log in the table
        ErrorLogs.objects.create(
            user_profile=user_profile,
            error_code=error_id,
            debug_log=debug_log,
            extra_debug_information=error_type,
            request_body=request_body,
        )

        return {
            "error_id": error_id,
            "debug_log": str(debug_log),
            "user_interface_message": message,
        }


class FrontendErrors(models.Model):

    api_code = models.CharField(max_length=10)
    error_datetime = models.DateTimeField(auto_now_add=True)
    error_description = models.TextField(null=True)
    error_type = models.CharField(max_length=100, null=False)
    priority = EnumField(
        choices=["default", "low", "medium", "high"], default="default", null=False
    )
    resolution_status = EnumField(
        choices=["not_resolved", "being_resolved", "resolved", "for_later"],
        default="not_resolved",
        null=False,
    )
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    screen = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "frontend_errors"
