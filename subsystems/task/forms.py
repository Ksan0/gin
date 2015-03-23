from gin.forms import GinForm
from django import forms


class CreateTaskForm(GinForm):
    text = forms.CharField(widget=forms.Textarea({"class": "text"}), min_length=10, max_length=255)
    
    def __init__(self, *args, **kwargs):
        super(CreateTaskForm, self).__init__("ajax_create_task", "POST", "", *args, **kwargs)


class AssignSelfTaskForm(GinForm):
    pass