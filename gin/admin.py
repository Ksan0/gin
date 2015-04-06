from django.contrib import admin
from subsystems.a_user.models import AUser
from subsystems.operator.models import OperatorInfo
from subsystems.task.models import Task
from subsystems.user.models import UserInfo


@admin.register(AUser)
class AUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_operator')
    #fields = ('email', 'first_name', 'last_name', 'is_operator', 'groups')


@admin.register(OperatorInfo)
class OperatorInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'active_tasks_count')
    list_editable = ('active_tasks_count',)

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'telephone', 'note')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'operator', 'text', 'creation_date', 'status', 'price_count')