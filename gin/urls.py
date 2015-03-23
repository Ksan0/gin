from django.conf.urls import patterns, include, url
from django.contrib import admin
import gin
from subsystems import user, task, dialog

urlpatterns = patterns(
    '',

    # ajax
    url(r"^ajax/signup_user$", user.views.ajax_signup, name="ajax_signup_user"),
    url(r"^ajax/signin_user$", user.views.ajax_signin, name="ajax_signin_user"),
    url(r"^ajax/create_task$", task.views.ajax_create_task, name="ajax_create_task"),
    url(r"^ajax/assign_self_task$", task.views.ajax_assign_self_task, "ajax_assign_self_task"),
    url(r"^ajax/add_message", dialog.views.ajax_add_message, name="ajax_add_message"),

    # views
    url(r"^$", gin.views.view_index),
    url(r"^task/(?P<task_id>\d+)$", task.views.view_task, name="view_task"),

    url(r'^admin/', include(admin.site.urls)),
)
