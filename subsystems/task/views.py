from subsystems.a_user.models import AUser
from subsystems.dialog.models import Message
from subsystems.operator.models import Operator
from subsystems.task.models import Task
from subsystems.utils.db import check_len
from subsystems.utils.json import render_to_json, AjaxStatus, AjaxErrors


def ajax_create_task(request):
    """
        === INPUT ===
            method: POST
            "text": текст задания
        === OUTPUT ===
            status: LoginError
            "task_id": номер созданного таска
            "creation_date":
            "text":
    """

    if request.method != "POST":
        return render_to_json(AjaxErrors.BAD_METHOD.json())

    if not request.user.is_authenticated():
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    try:
        form_text = check_len(request.POST.__getitem__("text"), 255, 1)
    except:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    try:
        task = Task(user=request.user, text=form_text)
        task.save()

        message = Message(task=task, user=request.user, body=form_text)
        message.save()
    except:
        return render_to_json(AjaxErrors.INTERNAL_ERROR.json())

    response_data = {
        "task_id": task.id,
        "creation_date": task.get_date_str(),
        "text": task.text
    }
    response_data.update(AjaxErrors.NONE.json())

    return render_to_json(response_data)


def ajax_get_task(request):
    if not request.user.is_authenticated():
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    user = AUser.objects.get(id=request.user.id)
    if not user.is_operator:
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    operator = Operator.objects.get(user=user)
    if operator.active_tasks_count >= 3:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    tasks = Task.objects.filter(operator=None, status=Task.Status.CREATED)
    if len(tasks) <= 0:
        return render_to_json(AjaxErrors.INTERNAL_ERROR.json())

    task = tasks[0]
    task.operator = operator
    task.save()
    operator.active_tasks_count += 1
    operator.save()

    response_data = {
        "task_id": task.id,
        "text": task.text,
        "date": task.get_date_str()
    }
    response_data.update(AjaxErrors.NONE.json())

    return render_to_json(response_data)


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
