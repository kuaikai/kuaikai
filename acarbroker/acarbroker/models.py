"""

SCL <scott@rerobots.net>
2018
"""
from __future__ import absolute_import

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    picture_url = models.URLField()
    display_name = models.CharField(max_length=128)


class SimJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    starttime = models.DateTimeField(auto_now_add=True, editable=False)
    stoptime = models.DateTimeField(null=True)
    done = models.BooleanField(default=False)
    result = models.CharField('outcome (result) of this job', max_length=8)
