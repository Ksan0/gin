from subsystems.dialog.models import Message
from subsystems.task.models import Task
from subsystems.utils.db import check_len
from subsystems.utils.json import render_to_json, AjaxPostErrors


def ajax_add_message(request):
    """
        === INPUT ===
            method: POST
            "task_id": id таска к которому добавляем сообщение
            "text"
        === OUTPUT ===
            status: AjaxError
    """

    if not request.user.is_authenticated():
        return render_to_json(AjaxPostErrors.BAD_SESSION.json())

    if request.method != "POST":
        return render_to_json(AjaxPostErrors.BAD_METHOD.json())

    try:
        task_id = request.POST.__getitem__("task_id")
        text = check_len(request.POST.__getitem__("text"), 255)
        task = Task.objects.get(id=task_id)
    except:
        return render_to_json(AjaxPostErrors.BAD_FORM.json())

    if request.user != task.user and request.user != task.operator.user and (not request.user.is_superuser):
        return render_to_json(AjaxPostErrors.BAD_SESSION.json())

    message = Message(task=task, user=request.user, body=text)
    message.save()

    return render_to_json(AjaxPostErrors.NONE.json())
