from django.db import models
from django.contrib.auth.models import User
import uuid
from django_mysql.models import EnumField

from config.helper_functions import format_date
from users.models import UserProfile


class Notes(models.Model):

    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)

    class Meta:
        db_table = "notes"

    def to_dict(self, summary_only=False):
        """Returns the dict object of a UserProfile object
        
        Returns:
            [dict]: The dict of the UserProfile object
        """

        user_dict = {
            "id": self.id,
            "title": self.title
        }
        
        if summary_only:
            return user_dict
        
        user_dict["description"] = self.description

        return user_dict
    
    