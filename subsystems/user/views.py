from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .view_ajax import *


def view_restore_password_confirm(request):
    context = {
        "restore_password_confirm_form": RestorePasswordConfirmForm(initial={
            'user_id': request.GET['uid'],
            'token': request.GET['token']
        })
    }

    return render(request, "restore_password_confirm.html", context)


def view_logout(request):
    logout(request)
    return redirect("/")