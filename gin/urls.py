from django.conf.urls import patterns, include, url
from django.contrib import admin
import gin
from subsystems import user, task, dialog

urlpatterns = patterns(
    '',

    # ajax
    url(r"^ajax/signup_user$", user.views.ajax_signup, name="ajax_signup_user"),
    url(r"^ajax/signin_user$", user.views.ajax_signin, name="ajax_signin_user"),
    url(r"^ajax/restore_password$", user.views.ajax_restore_password, name="ajax_restore_password"),
    url(r"^ajax/restore_password_confirm$", user.views.ajax_restore_password_confirm, name="ajax_restore_password_confirm"),
    url(r"^ajax/create_task$", task.views.ajax_create_task, name="ajax_create_task"),
    url(r"^ajax/assign_self_task$", task.views.ajax_assign_self_task, name="ajax_assign_self_task"),
    url(r"^ajax/set_price$", task.views.ajax_set_price, name="ajax_set_price"),
    url(r"^ajax/add_message", dialog.views.ajax_add_message, name="ajax_add_message"),

    # views
    url(r"^$", gin.views.view_index, name="view_index"),
    url(r"^task/(?P<task_id>\d+)$", task.views.view_task, name="view_task"),
    url(r"^faq$", gin.views.view_faq, name="view_faq"),
    url(r"^restore_password_confirm$", user.views.restore_password_confirm),
    url(r"^logout$", user.views.view_logout, name="view_logout"),
    # url(r"^admin$", gin.views.index_main_admin_page, name="index_main_admin_page"),

    # test
    url(r"^test_create$", gin.views.test_create),

    url(r'^admin/', include(admin.site.urls)),
)
