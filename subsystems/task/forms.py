from gin.forms import GinForm
from django import forms


class CreateTaskForm(GinForm):
    text = forms.CharField(
        label="",
        widget=forms.Textarea({"class": "text form-control"}),
        min_length=10,
        max_length=255,
        error_messages={
            'min_length': 'Опишите задачу подробнее'
        }
    )
    
    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_create_task")
        self.set_submit_button("Отправить")


class AssignSelfTaskForm(GinForm):
    def __init__(self, *args, **kwargs):
        super(AssignSelfTaskForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_assign_self_task")
        self.set_submit_button("Взять задачу")


class CreateTaskMessageForm(GinForm):
    text = forms.CharField(label="", widget=forms.Textarea({"class": "text ground__dialog__input__add-msg-form__txtarea form-control", "rows": "2"}))
    task_id = forms.IntegerField(widget=forms.HiddenInput(), label='')

    def __init__(self, *args, **kwargs):
        super(CreateTaskMessageForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_create_task_message")
        self.set_submit_button("Отправить", "ground__dialog__input__add-msg-form")


class SetPriceForm(GinForm):
    price_title = forms.CharField()
    price_count = forms.IntegerField()
    task_id = forms.IntegerField(widget=forms.HiddenInput(), label="")

    def __init__(self, *args, **kwargs):
        super(SetPriceForm, self).__init__("ajax_set_price", "POST", "", "set-price-btn", "Выставить счет", *args, **kwargs)