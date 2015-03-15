from django.db import models
from subsystems.a_user.models import AUser
from subsystems.task.models import Task


class Message(models.Model):
    task = models.ForeignKey(Task)       # таск, к которому привязано сообщение
    user = models.ForeignKey(AUser)      # юзер, который написал сообщение (может быть и оператором)
    body = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)

    def get_date_str(self):
        return '{:%d.%m.%Y %H:%M}'.format(self.creation_date)