from django.conf.urls import patterns, include, url
from django.contrib import admin
import gin
from subsystems import user, task
urlpatterns = patterns(
    '',

    # ========== AJAX ==========
    # ----- user -----
    url(r"^ajax/signup_user$", user.views.ajax_signup, name="ajax_signup_user"),
    url(r"^ajax/signin_user$", user.views.ajax_signin, name="ajax_signin_user"),
    url(r"^ajax/restore_password$", user.views.ajax_restore_password_request, name="ajax_restore_password_request"),
    url(r"^ajax/restore_password_confirm$", user.views.ajax_restore_password_confirm, name="ajax_restore_password_confirm"),
    # ----- task -----
    url(r"^ajax/create_task$", task.views.ajax_create_task, name="ajax_create_task"),
    url(r"^ajax/assign_self_task$", task.views.ajax_assign_self_task, name="ajax_assign_self_task"),
    url(r"^ajax/create_task_message", task.views.ajax_create_task_message, name="ajax_create_task_message"),
    url(r"^ajax/get_task_messages$", task.views.ajax_get_task_messages, name="ajax_get_task_messages"),
    url(r"^ajax/set_task_price$", task.views.ajax_set_task_price, name="ajax_set_task_price"),

    # ========== VIEWS ==========
    url(r"^$", gin.views.view_index, name="view_index"),
    url(r"^task/(?P<task_id>\d+)$", task.views.view_task, name="view_task"),
    url(r"^faq$", gin.views.view_faq, name="view_faq"),
    url(r"^restore_password_confirm$", user.views.view_restore_password_confirm),
    url(r"^logout$", user.views.view_logout, name="view_logout"),
    #url(r"^history$", gin.views.view_history, name="view_history"),

    # test
    url(r"^test_create$", gin.views.test_create),

    # url(r'^admin/', include(admin.site.urls)),
)

