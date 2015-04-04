from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from subsystems.a_user.models import AUser
from subsystems.task.models import Task, TaskManager
from subsystems.task.utils import get_task_history
from .view_ajax import *


def view_task(request, task_id):
    if not request.user.is_authenticated():
        return redirect("/")

    try:
        task = Task.objects.get(id=task_id)
    except:
        return redirect("/")

    if task.user != request.user and task.operator != request.user and not request.user.is_superuser:
        return redirect("/")

    paginator = Paginator(TaskMessage.objects.filter(task=task).order_by("creation_date"), 25)
    try:
        raw_messages = paginator.page(request.GET['p'])
    except:
        raw_messages = paginator.page(paginator.num_pages)

    messages = []
    for msg in raw_messages:
        messages.append({
            "class": msg.user.id == request.user.id and "dialog__msgright warning" or "dialog__msgleft success",
            "text": msg.body,
            "date": msg.get_date_str()
        })

    context = {
        "task_id": task.id,
        "messages": messages,
        "page": raw_messages,

        "set_price_form": SetPriceForm(initial={
            'task_id': task.id,
            'price_title': task.price_title,
            'price_count': task.price_count
        }),
        "add_message_form": CreateTaskMessageForm(initial={'task_id': task.id})
    }

    context.update(get_task_history(request.user))

    return render(request, "task.html", context)