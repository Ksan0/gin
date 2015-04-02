from subsystems.dialog.forms import AddMessageForm
from subsystems.dialog.models import Message
from subsystems.task.models import Task
from subsystems.utils.ajax import AjaxResponseKeys
from subsystems.utils.json import render_to_json, AjaxErrors


def ajax_add_message(request):
    form = AddMessageForm(request.POST or None)

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

    message = Message(task=task, user=request.user, body=s_text)
    message.save()

    response_data = {
        AjaxResponseKeys.CREATION_ID: message.id,
        AjaxResponseKeys.CREATION_DATA: s_text,
        AjaxResponseKeys.CREATION_DATE: message.get_date_str(),
        "class": "dialog__msgright warning"
    }
    return render_to_json(response_data)
