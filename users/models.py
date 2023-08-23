from urllib.request import Request
from django.db import models
from django.contrib.auth.models import User
import uuid
from django_mysql.models import EnumField

from config.helper_functions import format_date





class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    class Meta:
        db_table = "user_profile"

    def to_dict(self):
        """Returns the dict object of a UserProfile object
        
        Returns:
            [dict]: The dict of the UserProfile object
        """

        user_dict = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }

        return user_dict
    
