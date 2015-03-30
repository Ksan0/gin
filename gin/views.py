from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from subsystems.a_user.models import AUser
from subsystems.operator.models import Operator
from subsystems.task.forms import CreateTaskForm, AssignSelfTaskForm
from subsystems.task.models import Task, TaskManager
from subsystems import user


def index_hello_page(request):
    context = {
        "current_page": "index",
        "signup_form": user.forms.SignupForm(),
        "signin_form": user.forms.SigninForm(),
        "restore_password_form": user.forms.RestorePasswordForm()
    }
    return render(request, "hello.html", context)


def index_main_user_page(request):
    all_history_tasks = Task.objects.filter(user=request.user).order_by("-creation_date")
    last_open_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, True), 10)
    last_close_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, False), 10)
    context = {
        "current_page": "index",
        "last_open_tasks": last_open_tasks.page(1),
        "last_close_tasks": last_close_tasks.page(1),
        "create_task_form": CreateTaskForm()
    }
    return render(request, "main_user.html", context)


def index_main_operator_page(request):
    all_history_tasks = Task.objects.filter(operator=request.user.id).order_by("-creation_date")
    last_open_tasks = TaskManager.filter_by_status(all_history_tasks, True)[:10]
    last_close_tasks = TaskManager.filter_by_status(all_history_tasks, False)[:10]
    context = {
        "current_page": "index",
        "last_open_tasks": last_open_tasks,
        "last_close_tasks": last_close_tasks,
        "assign_self_task_form": AssignSelfTaskForm()
    }
    return render(request, "main_operator.html", context)


def index_main_admin_page(request):
    return render(request, "admin.html")


def view_index(request):
    if request.user.is_authenticated():
        if request.user.is_superuser:
            return index_main_admin_page(request)
        user = AUser.objects.get(id=request.user.id)
        if user.is_operator:
            return index_main_operator_page(request)
        else:
            return index_main_user_page(request)
    else:
        return index_hello_page(request)


def test_create(request):
    who = request.GET['who']

    if who == 'operator':
        i = len(Operator.objects.all())
        email = "op{0}@op.ru".format(i)
        u = AUser.objects.create_user(email=email, password="1", is_operator=True, is_superuser=False)
        o = Operator.objects.create(user=u)
        u = authenticate(id=u.id, password="1")
        login(request, u)
        return redirect("/")

    return redirect("/")

def view_faq(request):
    context = {
        "current_page": "faq",
        "signup_form": user.forms.SignupForm(),
        "signin_form": user.forms.SigninForm(),
        "restore_password_form": user.forms.RestorePasswordForm()
    }
    return render(request, "faq.html", context)