from subsystems.dialog.models import Message
from subsystems.task.models import Task
from subsystems.utils.db import check_len
from subsystems.utils.json import render_to_json, AjaxErrors


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
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    if request.method != "POST":
        return render_to_json(AjaxErrors.BAD_METHOD.json())

    try:
        task_id = request.POST.__getitem__("task_id")
        text = check_len(request.POST.__getitem__("text"), 255)
        task = Task.objects.get(id=task_id)
    except:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    if request.user != task.user and request.user != task.operator.user and (not request.user.is_superuser):
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    message = Message(task=task, user=request.user, body=text)
    message.save()

    response_data = {
        "text": text,
        "date": message.get_date_str(),
        "is_operator": message.user.is_operator
    }
    response_data.update(AjaxErrors.NONE.json())

    return render_to_json(response_data)


def ajax_get_messages(request):
    """
        === INPUT ===
            method: GET
            "task_id"
            "page"
        === OUTPUT ===
            status: AjaxError
            "messages"
    """

    if not request.user.is_authenticated():
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    try:
        task_id = request.GET["task_id"]
        page = int(request.GET["page"])
        task = Task.objects.get(id=task_id)
        if task.user != request.user:
            return render_to_json(AjaxErrors.BAD_SESSION.json())

        messages = Message.objects.filter(task=task).order_by("creation_date")[page*10:(page+1)*10]
        messages_json = []
        for msg in messages:
            messages_json.append({
                "is_operator": msg.user.is_operator,
                "text": msg.body,
                "date": msg.get_date_str()
            })
    except:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    return render_to_json({
        "page": page,
        "messages_count": len(messages_json),
        "messages": messages_json
    })