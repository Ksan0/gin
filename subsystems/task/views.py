from subsystems.dialog.models import Message
from subsystems.task.models import Task
from subsystems.utils.db import check_len
from subsystems.utils.json import render_to_json, AjaxStatus, AjaxPostErrors


def ajax_create_task(request):
    """
        === INPUT ===
            method: POST
            "text": текст задания
        === OUTPUT ===
            status: LoginError
            "task_id": номер созданного таска
    """

    class AjaxErrors(AjaxPostErrors):
        pass

    if request.method != "POST":
        return render_to_json(AjaxErrors.BAD_METHOD.json())

    if not request.user.is_authenticated():
        return render_to_json(AjaxErrors.BAD_SESSION.json())

    try:
        form_text = check_len(request.POST.__getitem__("text"), 255)
    except:
        return render_to_json(AjaxErrors.BAD_FORM.json())

    try:
        task = Task(user=request.user)
        task.save()

        message = Message(task=task, user=request.user, body=form_text)
        message.save()
    except:
        return render_to_json(AjaxErrors.INTERNAL_ERROR.json())

    response_data = {
        "task_id": task.id
    }
    response_data.update(AjaxErrors.NONE.json())

    return render_to_json(response_data)
