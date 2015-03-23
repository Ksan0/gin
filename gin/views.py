from django.contrib.auth import authenticate, login, logout
from django.core.context_processors import csrf
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from subsystems.a_user.models import AUser
from subsystems.operator.models import Operator
from subsystems.task.forms import CreateTaskForm
from subsystems.task.models import Task, TaskManager
from subsystems import user


def index_hello_page(request):
    context = {
        "signup_form": user.forms.SignupForm(),
        "signin_form": user.forms.SigninForm()
    }
    return render(request, "main.html", context)


def index_main_user_page(request):
    all_history_tasks = Task.objects.filter(user=request.user).order_by("-creation_date")
    last_open_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, True), 10)
    last_close_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, False), 10)
    context = {
        "last_open_tasks": last_open_tasks.page(1),
        "last_close_tasks": last_close_tasks.page(1),
        "create_task_form": CreateTaskForm()
    }
    return render(request, "page.html", context)


def index_main_operator_page(request):
    operator = Operator.objects.get(user=request.user)
    all_history_tasks = Task.objects.filter(operator=operator).order_by("-creation_date")
    last_open_tasks = TaskManager.filter_by_status(all_history_tasks, True)[:10]
    last_close_tasks = TaskManager.filter_by_status(all_history_tasks, False)[:10]
    context = {
        "last_open_tasks": last_open_tasks,
        "last_close_tasks": last_close_tasks
    }
    return render(request, "operator.html", context)


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


def view_task(request):
    """
        === INPUT ===
            task_id
    """

    task_id = request.GET["task_id"]

    try:
        task = Task.objects.get(id=task_id)
        if task.user != request.user and task.operator.user != request.user:
            return redirect("/")
    except:
        return redirect("/")

    u = AUser.objects.get(id=request.user.id)

    context = {
        "task_id": task.id,
        "is_operator": u.is_operator,
        "price": task.price
    }

    return render(request, "dialog.html", context)








def test_createoperator(request):
    if request.user.is_authenticated():
        logout(request)

    u = AUser.objects.create_user(password="1", is_operator=True)

    u = authenticate(id=u.id, password="1")
    login(request, u)

    x = Operator.objects.create(user=u)
    x.save()

    return redirect("/")





def createsuper2(request):
    u = AUser.objects.create_user(password="1", is_superuser=True)
    u = authenticate(id=u.id, password="1")
    login(request, u)
    return redirect("/")


def createuser(request):
    u = AUser.objects.create_user(password="1", is_superuser=False)
    u = authenticate(id=u.id, password="1")
    login(request, u)
    return redirect("/")


def index2(request):
    # a_user = User.objects.create_superuser(password="123")

    context = {}
    context.update(csrf(request))

    return render(request, "signup.html", context)


def main2(request):
    return render(request, "main.html")


def page2(request):
    return render(request, "page.html")


def dialog2(request):
    return render(request, "dialog.html")


def paypal2(request):
    return render(request, "paypal.html")


def test2(request):
    #u = authenticate(id=1, password="1")
    #login(request, u)

    request.user.email_user(subject="ololo", message="alala")

    c = {
        "super": request.user.is_superuser
    }
    return render(request, "test.html", c)