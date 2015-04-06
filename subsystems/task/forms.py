from gin.forms import GinForm
from django import forms
from gin.settings_db import SettingsDB


class CreateTaskForm(GinForm):
    text = forms.CharField(
        label="",
        max_length=SettingsDB.MAX_TASK_MESSAGE_LENGTH,
        widget=forms.Textarea({
            "placeholder": "Опишите тут ваше задание...",
            "class": "text form-control"
        }),
        error_messages={
            'min_length': 'Опишите задачу подробнее'
        }
    )

    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_create_task")
        self.set_on_ctrl_enter(True)
        self.set_submit_button("Отправить")


class AssignSelfTaskForm(GinForm):
    def __init__(self, *args, **kwargs):
        super(AssignSelfTaskForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_assign_self_task")
        self.set_submit_button("Взять задачу")


class CreateTaskMessageForm(GinForm):
    text = forms.CharField(
        label="",
        max_length=SettingsDB.MAX_TASK_MESSAGE_LENGTH,
        widget=forms.Textarea({
            "placeholder": "Текст вашего сообщения...",
            "class": "text ground__dialog__input__add-msg-form__txtarea form-control",
            "rows": "3"
        })
    )
    task_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CreateTaskMessageForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_create_task_message")
        self.set_submit_button("Отправить")
        self.set_on_ctrl_enter(True)
        self.set_field_wrapper_class("text", "span8")
        self.set_field_wrapper_class("submit_button", "span1")


class GetTaskMessagesForm(GinForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput())
    last_download_message_id = forms.IntegerField(
        label="",
        widget=forms.HiddenInput(attrs={"class": "last_download_message_id"}),
        initial=-1
    )

    def __init__(self, *args, **kwargs):
        super(GetTaskMessagesForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_get_task_messages")
        self.set_submit_button("Показать предыдущие сообщения")
        self.set_send_on_init(True)


class TaskPriceForm(GinForm):
    price_title = forms.CharField(
        label="Наименование товара",
        max_length=SettingsDB.MAX_TASK_PRICE_TITLE
    )
    price_count = forms.IntegerField(
        label="Цена (руб)",
        min_value=0
    )
    task_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(TaskPriceForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_set_task_price")
        self.set_submit_button("Выставить счет", "set-price-btn")


class CloseTaskForm(GinForm):
    task_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(CloseTaskForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_close_task")
        self.set_submit_button("Закрыть задачу")