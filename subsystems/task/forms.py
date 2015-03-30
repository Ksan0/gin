from gin.forms import GinForm
from django import forms


class CreateTaskForm(GinForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea({"class": "text form-control"}),
        min_length=10,
        max_length=255,
        error_messages={
            'min_length': '    Желания менее 10 символов не исполняются'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__("ajax_create_task", "POST", "", "", "Отправить", *args, **kwargs)


class AssignSelfTaskForm(GinForm):
    def __init__(self, *args, **kwargs):
        super(AssignSelfTaskForm, self).__init__("ajax_assign_self_task", "POST", "", "", "Взять задачу", *args, **kwargs)


class SetPriceForm(GinForm):
    price_title = forms.CharField()
    price_count = forms.IntegerField()
    task_id = forms.IntegerField(widget=forms.HiddenInput(), label="")

    def __init__(self, *args, **kwargs):
        super(SetPriceForm, self).__init__("ajax_set_price", "POST", "", "", "Выставить счет", *args, **kwargs)