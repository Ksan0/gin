from django.db import models
from subsystems.a_user.models import AUser


class OperatorInfo(models.Model):
    user = models.ForeignKey(AUser)
    active_tasks_count = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.user)