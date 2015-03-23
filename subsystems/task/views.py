from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect, render
from subsystems.a_user.models import AUser
from subsystems.dialog.models import Message
from subsystems.operator.models import Operator
from subsystems.task.forms import CreateTaskForm, AssignSelfTaskForm
from subsystems.task.models import Task, TaskManager
from subsystems.utils.ajax import AjaxResponseKeys
from subsystems.utils.json import render_to_json


def ajax_create_task(request):
    form = CreateTaskForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not request.user.is_authenticated():
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_text = form.cleaned_data['text']
        task = Task(user=request.user, text=s_text)
        task.save()

        message = Message(task=task, user=request.user, body=s_text)
        message.save()
    except:
        form.add_error(None, "internal error")
        return render_to_json(form.errors_to_json())

    response_data = {
        AjaxResponseKeys.CREATION_ID: task.id,
        AjaxResponseKeys.CREATION_DATA: task.text,
        AjaxResponseKeys.CREATION_DATE: task.get_date_str()
    }
    return render_to_json(response_data)


def ajax_assign_self_task(request):
    form = AssignSelfTaskForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not request.user.is_authenticated():
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    try:
        operator = Operator.objects.get(user=request.user.id)
    except:
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if operator.active_tasks_count >= 3:
        form.add_error(None, "Достигнуто максимальное количество активных задач")
        return render_to_json(form.errors_to_json())

    tasks = Task.objects.filter(operator=None, status=Task.Status.CREATED)
    if len(tasks) <= 0:
        form.add_error(None, "Очередь задач пуста")
        return render_to_json(form.errors_to_json())

    task = tasks[0]
    task.operator = operator
    task.save()
    operator.active_tasks_count += 1
    operator.save()

    response_data = {
        AjaxResponseKeys.CREATION_ID: task.id,
        AjaxResponseKeys.CREATION_DATA: task.text,
        AjaxResponseKeys.CREATION_DATE: task.get_date_str()
    }
    return render_to_json(response_data)


def view_task(request, task_id):
    if not request.user.is_authenticated():
        return redirect("/")

    try:
        task = Task.objects.get(id=task_id)
    except:
        return redirect("/")

    if task.user.id != request.user.id and task.operator.id != request.user.id and not request.user.is_superuser:
        return redirect("/")

    user = AUser.objects.get(id=request.user.id)

    paginator = Paginator(Message.objects.filter(task=task), 1)
    try:
        raw_messages = paginator.page(request.GET['p'])
    except EmptyPage:
        raw_messages = paginator.page(paginator.num_pages)
    except:
        raw_messages = paginator.page(1)

    messages = []
    for msg in raw_messages:
        messages.append({
            "class": msg.user.id == request.user.id and "dialog__msgright bg-warning" or "dialog__msgleft bg-success",
            "text": msg.body,
            "date": msg.get_date_str()
        })

    all_history_tasks = Task.objects.filter(user=request.user).order_by("-creation_date")
    last_open_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, True), 10)
    last_close_tasks = Paginator(TaskManager.filter_by_status(all_history_tasks, False), 10)

    context = {
        "task_id": task.id,
        "is_operator": user.is_operator,
        "messages": messages,
        "paginator": raw_messages,
        "price": task.price,

        "last_open_tasks": last_open_tasks.page(1),
        "last_close_tasks": last_close_tasks.page(1)
    }

    return render(request, "task.html", context)

"""
def ajax_set_price(request):
    if request.method != "POST":
        return render_to_json(AjaxErrors.BAD_METHOD.json())

    if not request.user.is_authenticated():
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    user = AUser.objects.get(id=request.user.id)
    if not user.is_operator:
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    try:
        price = request.POST.__getitem__("price")
        task_id = request.POST.__getitem__("task_id")
        task = Task.objects.get(id=task_id)
    except:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    if task.operator != user.operator:
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    task.price = price
    task.status = Task.Status.SOLVED
    task.save()
    task.operator.active_tasks_count -= 1
    task.operator.save()

    response_data = {
        "price": price
    }
    response_data.update(AjaxErrors.NONE.json())
    return render_to_json(response_data)
"""