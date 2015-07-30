from django.db import models
from django.contrib.auth.models import User
from management.models import Organization


class UserProfile(models.Model):
    """User profiles"""
    profile = models.Manager()
    user = models.OneToOneField(User)
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.user.username
