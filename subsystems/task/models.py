from django.db import models
from django.utils.datetime_safe import datetime
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
        CREATE = 0                  # таск был создан, но его еще не распределили оператору
        ASSIGN = 1                  # оператор получил этот таск
        HAVE_PRICE = 2              # счет выставлен
        # close
        CANCEL_BY_USER = 50         # юзер отменил таск
        CANCEL_BY_OPERATOR = 51     # оператор отменил таск
        SOLVED = 52                 # таск решен

    objects = TaskManager()

    creation_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=Status.CREATE)
    user = models.ForeignKey(AUser, related_name='+')                       # юзер, который создал таск
    operator = models.ForeignKey(AUser, null=True, related_name='+')        # оператор, который выполняет таск
    text = models.CharField(max_length=255)

    price_title = models.CharField(default="", max_length=50)
    price_count = models.IntegerField(default=0)

    def get_date_str(self):
        today = datetime.now()
        if today.day != self.creation_date.day or today.month != self.creation_date.month \
                or today.year != self.creation_date.year:
            return '{:%d.%m.%Y}'.format(self.creation_date)
        else:
            return '{:%H:%M}'.format(self.creation_date)