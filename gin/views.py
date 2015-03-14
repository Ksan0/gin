from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.shortcuts import render, redirect
from subsystems.a_user.models import AUser
from subsystems.task.models import Task


def index_hello_page(request):
    return render(request, "main.html")


def index_main_page(request):
    all_history_tasks = Task.objects.filter(user=request.user).order_by("creation_date")
    last10_solved = all_history_tasks.filter(status=Task.Status.SOLVED)
    context = {
        "history_tasks": history_tasks
    }
    return render(request, "page.html", context)


def view_index(request):
    if request.user.is_authenticated():
        return index_main_page(request)
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
        if task.user != request.user:
            return redirect("/")
    except:
        return redirect("/")

    return render(request, "dialog.html")

















def createsuper2(request):
    u = AUser.objects.create_user(password="1", is_superuser=True)
    u = authenticate(id=u.id, password="1")
    login(request, u)
    return render(request, "test.html")


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