from django.db import models
from subsystems.operator.models import Operator
from subsystems.a_user.models import AUser


class Task(models.Model):
    class Status(object):
        CREATED = 0             # таск был создан, но его еще не смотрел оператор
        LOOKED = 1              # оператор смотрел этот таск
        CANCEL_BY_USER = 2      # юзер отменил таск
        CANCEL_BY_OPERATOR = 3  # оператор отменил таск
        SOLVED = 4              # таск решен

    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=Status.CREATED)
    user = models.ForeignKey(AUser)                      # юзер, который создал таск
    operator = models.ForeignKey(Operator, null=True)   # оператор, на которого повесили таск

