from django.conf.urls import patterns, include, url
from django.contrib import admin
import gin
from subsystems import a_user, task, dialog


urlpatterns = patterns(
    '',

    # ajax
    url(r'^ajax/signup_user$', a_user.views.ajax_signup_user),
    url(r'^ajax/signin$', a_user.views.ajax_signin),
    url(r'^ajax/create_task$', task.views.ajax_create_task),
    url(r'^ajax/add_message$', dialog.views.ajax_add_message),
    url(r'^ajax/get_messages$', dialog.views.ajax_get_messages),

    # test
    url(r'^$', gin.views.view_index),
    #url(r'^task$', gin.views.dialog),
    #url(r'^paypal$', gin.views.paypal),
    #url(r'^test$', gin.views.test),
    #url(r'^createsuper$', gin.views.createsuper),

    url(r'^admin/', include(admin.site.urls)),
)
