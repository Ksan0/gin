from django.db import models
from subsystems.a_user.models import AUser


class Operator(models.Model):
    user = models.OneToOneField(AUser)
    active_tasks_count = models.SmallIntegerField(default=0)