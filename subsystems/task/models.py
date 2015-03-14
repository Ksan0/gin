from django.db import models
from subsystems.operator.models import Operator
from subsystems.a_user.models import AUser


class TaskManager(models.Manager):
    def filter_by_status(self, is_open):
        if is_open:
            index = Task.Status.OPEN_INDEX
        else:
            index = Task.Status.CLOSE_INDEX
        return self.filter(status__gte=index[0], status__lt=index[1])


class Task(models.Model):
    class Status(object):
        # low <= index < high
        OPEN_INDEX = (0, 50)
        CLOSE_INDEX = (50, 100)
        # open
        CREATED = 0             # таск был создан, но его еще не смотрел оператор
        LOOKED = 1              # оператор смотрел этот таск
        # close
        CANCEL_BY_USER = 50      # юзер отменил таск
        CANCEL_BY_OPERATOR = 51  # оператор отменил таск
        SOLVED = 52              # таск решен

    objects = TaskManager()

    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=Status.CREATED)
    user = models.ForeignKey(AUser)                      # юзер, который создал таск
    operator = models.ForeignKey(Operator, null=True)   # оператор, на которого повесили таск

