from django.db import models
from subsystems.a_user.models import AUser


class User(models.Model):
    user = models.OneToOneField(AUser)
    address = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)