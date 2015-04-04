from .models import Task, TaskMessage
from .forms import CreateTaskForm, AssignSelfTaskForm, SetPriceForm, CreateTaskMessageForm, GetTaskMessagesForm
from subsystems.operator.models import OperatorInfo
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

        message = TaskMessage(task=task, user=request.user, body=s_text)
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
        operator = OperatorInfo.objects.get(user=request.user.id)
    except:
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if operator.active_tasks_count >= 10:
        form.add_error(None, "Достигнуто максимальное количество активных задач")
        return render_to_json(form.errors_to_json())

    tasks = Task.objects.filter(operator=None, status=Task.Status.CREATE).order_by("creation_date")
    try:
        task = tasks[0]
    except:
        form.add_error(None, "Очередь задач пуста")
        return render_to_json(form.errors_to_json())

    task.operator = request.user
    task.status = Task.Status.ASSIGN
    task.save()
    operator.active_tasks_count += 1
    operator.save()

    response_data = {
        AjaxResponseKeys.CREATION_ID: task.id,
        AjaxResponseKeys.CREATION_DATA: task.text,
        AjaxResponseKeys.CREATION_DATE: task.get_date_str()
    }
    return render_to_json(response_data)


def ajax_create_task_message(request):
    form = CreateTaskMessageForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not request.user.is_authenticated():
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_task_id = form.cleaned_data['task_id']
        task = Task.objects.get(id=s_task_id)
    except:
        form.add_error(None, "bad task id")
        return render_to_json(form.errors_to_json())

    if task.user.id != request.user.id and task.operator.id != request.user.id and not request.user.is_superuser:
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    s_text = form.cleaned_data['text']

    message = TaskMessage(task=task, user=request.user, body=s_text)
    message.save()

    response_data = {
        AjaxResponseKeys.CREATION_ID: message.id,
        AjaxResponseKeys.CREATION_DATA: s_text,
        AjaxResponseKeys.CREATION_DATE: message.get_date_str(),
        "class": "dialog__msgright warning"
    }
    return render_to_json(response_data)


def ajax_get_task_messages(request):
    form = GetTaskMessagesForm(request.POST)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not request.user.is_authenticated():
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_task_id = form.cleaned_data['task_id']
        task = Task.objects.get(id=s_task_id)
    except:
        form.add_error(None, "internal error")
        return render_to_json(form.errors_to_json())

    if task.user.id != request.user.id and task.operator.id != request.user.id and not request.user.is_superuser:
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    MESSAGES_CHUNK = 25

    try:
        s_last_download_message_id = form.cleaned_data['last_download_message_id']
        messages = TaskMessage.objects.filter(task=task)
        if s_last_download_message_id != -1:
            messages = TaskMessage.objects.filter(id__lt=s_last_download_message_id)
        messages = messages.order_by("-id")[:MESSAGES_CHUNK]
    except:
        form.add_error(None, "empty dd")
        return render_to_json(form.errors_to_json())

    response_data = {
        "count": len(messages),
        "data": [],
        "last_download_message_id": -1
    }

    if response_data["count"] == MESSAGES_CHUNK:
        response_data["last_download_message_id"] = messages[response_data["count"]-1].id

    for msg in messages:
        response_data["data"].append({
            "class": msg.user == request.user and "dialog__msgright warning" or "dialog__msgleft success",
            "text": msg.body,
            "date": msg.get_date_str()
        })

    return render_to_json(response_data)


def ajax_set_price(request):
    form = SetPriceForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not request.user.is_authenticated():
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_task_id = form.cleaned_data['task_id']
        task = Task.objects.get(id=s_task_id)
    except:
        form.add_error(None, "bad task id")
        return render_to_json(form.errors_to_json())

    if task.operator.id != request.user.id and not request.user.is_superuser:
        form.add_error(None, "bad session")
        return render_to_json(form.errors_to_json())

    s_price_title = form.cleaned_data['price_title']
    s_price_count = form.cleaned_data['price_count']
    task.price_title = s_price_title
    task.price_count = s_price_count
    task.status = Task.Status.HAVE_PRICE
    task.save()

    response_data = {
        AjaxResponseKeys.CREATION_ID: task.id,
        "price_title": s_price_title,
        "price_count": s_price_count
    }
    return render_to_json(response_data)