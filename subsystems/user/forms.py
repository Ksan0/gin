from gin.forms import GinForm
from django import forms
from subsystems.user.utils import forms_clean_password


class SignupForm(GinForm):
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "youremail@super.ru", "class": ""}), label="Ваш email")
    password = forms.CharField(widget=forms.PasswordInput({"class": "", "klass": "aaa"}), label="Придумайте  пароль")
    password2 = forms.CharField(widget=forms.PasswordInput({"class": ""}), label="Повторите пароль")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_signup_user")
        self.set_submit_button("Зарегистрироваться")
        self.set_field_wrapper_class("email", "ololo")

    def clean_password(self):
        return forms_clean_password(self.data['password'], self.data['password2'])


class SigninForm(GinForm):
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "youremail@super.ru", "class": ""}), label="Ваш email")
    password = forms.CharField(widget=forms.PasswordInput({"class": ""}), label="Пароль")
    
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_signin_user")
        self.set_submit_button("Войти")


class RestorePasswordRequestForm(GinForm):
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "youremail@super.ru", "class": "form-control"}), label="Ваш email")

    def __init__(self, *args, **kwargs):
        super(RestorePasswordRequestForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_restore_password_request")
        self.set_submit_button("Восстановить", "btn-restore")


class RestorePasswordConfirmForm(GinForm):
    password = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}), label="Ваш пароль")
    password2 = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}), label="Повторите пароль")
    user_id = forms.IntegerField(widget=forms.HiddenInput(), label="")
    token = forms.CharField(widget=forms.HiddenInput(), label="")

    def __init__(self, *args, **kwargs):
        super(RestorePasswordConfirmForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_restore_password_confirm")
        self.set_submit_button("Сменить пароль")

    def clean_password(self):
        return forms_clean_password(self.data['password'], self.data['password2'])