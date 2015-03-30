from gin.forms import GinForm
from django import forms


class AddMessageForm(GinForm):
    text = forms.CharField(label="", widget=forms.Textarea({"class": "text ground__dialog__input__add-msg-form__txtarea form-control"}))
    task_id = forms.IntegerField(widget=forms.HiddenInput(), label='')

    def __init__(self, *args, **kwargs):
        super(AddMessageForm, self).__init__("ajax_add_message", "POST", "ground__dialog__input__add-msg-form", "", "Отправить", *args, **kwargs)