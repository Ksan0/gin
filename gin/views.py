from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from subsystems.a_user.models import AUser
from subsystems.operator.models import OperatorInfo
from subsystems.task.forms import CreateTaskForm, AssignSelfTaskForm
from subsystems import user
from subsystems.task.utils import get_task_history


def subview_index_anonymous(request, context):
    context.update({
        "signup_form": user.forms.SignupForm(),
        "signin_form": user.forms.SigninForm(),
        "restore_password_request_form": user.forms.RestorePasswordRequestForm()
    })
    return render(request, "pages/index_anonymous.html", context)


def subview_index_user(request, context):
    context.update({
        "create_task_form": CreateTaskForm()
    })
    return render(request, "pages/index_user.html", context)


def subview_index_operator(request, context):
    context.update({
        "assign_self_task_form": AssignSelfTaskForm()
    })
    return render(request, "pages/index_operator.html", context)


def view_index(request):
    context = {
        "current_view_name": "view_index"
    }

    if request.user.is_authenticated():
        context.update(get_task_history(request.user))

        if request.user.is_operator:
            return subview_index_operator(request, context)
        else:
            return subview_index_user(request, context)
    else:
        return subview_index_anonymous(request, context)


def view_faq(request):
    context = {
        "current_view_name": "view_faq",
        "signup_form": user.forms.SignupForm(),
        "signin_form": user.forms.SigninForm(),
        "restore_password_form": user.forms.RestorePasswordRequestForm()
    }
    return render(request, "pages/faq.html", context)


def test_create(request):
    who = request.GET['who']

    if who == 'operator':
        i = len(OperatorInfo.objects.all())
        email = "op{0}@op.ru".format(i)
        u = AUser.objects.create_user(email=email, password="1", is_operator=True, is_superuser=False)
        o = OperatorInfo.objects.create(user=u)
        u = authenticate(id=u.id, password="1")
        login(request, u)
        return redirect("/")

    return redirect("/")