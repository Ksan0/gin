from django import forms
from subsystems.utils.ajax import AjaxResponseKeys


class GinForm(forms.Form):
    def __init__(self, action_url_name, action_method, html_class, submit_button_class, submit_button_title, *args, **kwargs):
        super(GinForm, self).__init__(*args, **kwargs)

        self.__html_id = (self.__module__ + "_" + self.__class__.__name__).replace(".", "_")
        self.__html_class = html_class
        self.__submit_button_class = submit_button_class
        self.__submit_button_title = submit_button_title
        self.__action_url_name = action_url_name
        self.__action_method = action_method

    def html_id(self):
        return self.__html_id

    def html_class(self):
        return self.__html_class

    def submit_button_class(self):
        return self.__submit_button_class

    def submit_button_title(self):
        return self.__submit_button_title

    def action_method(self):
        return self.__action_method

    def action_url_name(self):
        return self.__action_url_name

    def errors_to_json(self):
        fields_errors = {}
        for e in self.errors:
            fields_errors[e] = self.errors[e][0]
            return {
                AjaxResponseKeys.FIELDS_ERRORS: fields_errors
            }