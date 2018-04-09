"""
Copyright (c) 2018， Silicon Valley Career Women.
All rights reserved.
"""
from django.db import models
from ..accounts.models import Profile


class Mentor(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile.user.username
