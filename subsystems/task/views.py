from django.shortcuts import redirect, render
from subsystems.task.forms import TaskPriceForm
from subsystems.task.utils import get_task_history
from subsystems.user.models import UserInfo
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

    client_user_info = UserInfo.objects.get(user=task.user)
    setattr(task, "userinfo", client_user_info)

    context = {
        "task": task,

        "assign_self_task_form": AssignSelfTaskForm(),
        "create_task_message_form": CreateTaskMessageForm(initial={'task_id': task.id}),
        "get_task_messages_form": GetTaskMessagesForm(initial={'task_id': task.id}),
        "task_price_form": TaskPriceForm(initial={
            'task_id': task.id,
            'price_title': task.price_title,
            'price_count': task.price_count
        }),
        "close_task_form": CloseTaskForm(initial={'task_id': task.id})
    }

    context.update(get_task_history(request.user))

    return render(request, "pages/task.html", context)