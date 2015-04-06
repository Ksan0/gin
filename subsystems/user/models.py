from django.db import models
from subsystems.a_user.models import AUser


class UserInfo(models.Model):
    user = models.ForeignKey(AUser)
    address = models.CharField(max_length=1024, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    note = models.TextField(max_length=2048, blank=True)