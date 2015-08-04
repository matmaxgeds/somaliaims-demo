from django.db import models
from django.contrib.auth.models import User
from management.models import Organization
from data_entry.models import UserOrganization


class UserProfile(models.Model):
    """User profiles"""
    profile = models.Manager()
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    organization2 = models.ForeignKey(UserOrganization,
                                      verbose_name="If the user's organizations is in the additional organizations list",
                                      blank=True, null=True)

    def __str__(self):
        return self.user.username
