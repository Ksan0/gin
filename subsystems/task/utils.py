from .models import Task, TaskManager


def get_task_history(user):
    if user.is_operator:
        all_history_tasks = Task.objects.filter(operator=user)
    else:
        all_history_tasks = Task.objects.filter(user=user)
    all_history_tasks = all_history_tasks.order_by("-creation_date")

    return {
        "last_open_tasks": TaskManager.filter_by_status(all_history_tasks, True)[:5],
        "last_close_tasks": TaskManager.filter_by_status(all_history_tasks, False)[:5]
    }