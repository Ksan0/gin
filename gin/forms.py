from django import forms
from subsystems.utils.ajax import AjaxResponseKeys
from django.template.defaulttags import register


class GinForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(GinForm, self).__init__(*args, **kwargs)

        self.__form_id = (self.__module__ + "_" + self.__class__.__name__).replace(".", "_")
        self.__form_class = ""

        self.__submit_button_class = ""
        self.__submit_button_title = ""

        self.__action_url_name = ""
        self.__action_method = "POST"

        self.__on_ctrl_enter = False
        self.__send_on_init = False
        # TODO:
        # переписать на виджетах
        self.__fields_wrapper_classes = {}

    def get_form_id(self):
        return self.__form_id

    def set_form(self, klass):
        self.__form_class = klass

    def get_form_class(self):
        return self.__form_class

    def set_submit_button(self, title, klass=None):
        self.__submit_button_title = title
        if klass is not None:
            self.__submit_button_class = klass

    def get_submit_button_class(self):
        return self.__submit_button_class

    def get_submit_button_title(self):
        return self.__submit_button_title

    def set_action(self, url_name, method=None):
        self.__action_url_name = url_name
        if method is not None:
            self.__action_method = method

    def get_action_method(self):
        return self.__action_method

    def get_action_url_name(self):
        return self.__action_url_name

    def set_on_ctrl_enter(self, v):
        self.__on_ctrl_enter = v

    def get_on_ctrl_enter(self):
        return self.__on_ctrl_enter

    def set_send_on_init(self, v):
        self.__send_on_init = v

    def get_send_on_init(self):
        return self.__send_on_init

    def set_field_wrapper_class(self, field, klass):
        self.__fields_wrapper_classes[field] = klass

    def get_field_wrapper_class(self, field):
        return self.__fields_wrapper_classes.get(field, "")

    def errors_to_json(self):
        fields_errors = {}
        for e in self.errors:
            fields_errors[e] = self.errors[e][0]
            return {
                AjaxResponseKeys.FIELDS_ERRORS: fields_errors
            }


@register.filter
def get_form_field_wrapper(form, field):
    if isinstance(field, str):
        return form.get_field_wrapper_class(field)
    return form.get_field_wrapper_class(field.name)
