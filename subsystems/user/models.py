from django.db import models
from subsystems.a_user.models import AUser


class User(models.Model):
    user = models.ForeignKey(AUser)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)