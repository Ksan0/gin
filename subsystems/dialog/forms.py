from gin.forms import GinForm
from django import forms


class AddMessageForm(GinForm):
    text = forms.CharField(widget=forms.Textarea({"class": "text"}))
    task_id = forms.IntegerField(widget=forms.HiddenInput(), label='')

    def __init__(self, *args, **kwargs):
        super(AddMessageForm, self).__init__("ajax_add_message", "POST", "", *args, **kwargs)