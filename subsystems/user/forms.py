from gin.forms import GinForm
from django import forms
from subsystems.user.utils import forms_clean_password
from gin.settings_db import SettingsDB


class SignupForm(GinForm):
    name = forms.CharField(
        label="Ваше имя",
        min_length=SettingsDB.MIN_NAME_LENGTH,
        max_length=SettingsDB.MAX_NAME_LENGTH,
        widget=forms.TextInput({
            "placeholder": "Дуся"
        })
    )
    email = forms.EmailField(
        label="Ваш email",
        max_length=SettingsDB.MAX_EMAIL_LENGTH,
        widget=forms.EmailInput({
            "placeholder": "youremail@super.ru"
        })
    )
    password = forms.CharField(
        label="Придумайте  пароль",
        min_length=SettingsDB.MIN_PASSWORD_LENGTH,
        max_length=SettingsDB.MAX_PASSWORD_LENGTH,
        widget=forms.PasswordInput(),
        error_messages={
            "min_length": "Пароль должен содержать как минимум 6 символов"
        }
    )
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Повторите пароль")

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_signup_user")
        self.set_submit_button("Зарегистрироваться")

    def clean_password(self):
        return forms_clean_password(self.data['password'], self.data['password2'])


class SigninForm(GinForm):
    email = forms.EmailField(
        label="Ваш email",
        max_length=SettingsDB.MAX_EMAIL_LENGTH,
        widget=forms.EmailInput({
            "placeholder": "youremail@super.ru"
        })
    )
    password = forms.CharField(
        label="Пароль",
        max_length=SettingsDB.MAX_PASSWORD_LENGTH,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_signin_user")
        self.set_submit_button("Войти")


class RestorePasswordRequestForm(GinForm):
    email = forms.EmailField(
        label="Ваш email",
        max_length=SettingsDB.MAX_EMAIL_LENGTH,
        widget=forms.EmailInput({
            "placeholder": "youremail@super.ru",
            "class": "form-control"
        })
    )

    def __init__(self, *args, **kwargs):
        super(RestorePasswordRequestForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_restore_password_request")
        self.set_submit_button("Восстановить", "btn-restore")


class RestorePasswordConfirmForm(GinForm):
    password = forms.CharField(
        label="Ваш пароль",
        min_length=SettingsDB.MIN_PASSWORD_LENGTH,
        max_length=SettingsDB.MAX_PASSWORD_LENGTH,
        widget=forms.PasswordInput({"class": "form-control"})
    )
    password2 = forms.CharField(widget=forms.PasswordInput({"class": "form-control"}), label="Повторите пароль")
    user_id = forms.IntegerField(widget=forms.HiddenInput(), label="")
    token = forms.CharField(widget=forms.HiddenInput(), label="")

    def __init__(self, *args, **kwargs):
        super(RestorePasswordConfirmForm, self).__init__(*args, **kwargs)
        self.set_action("ajax_restore_password_confirm")
        self.set_submit_button("Сменить пароль")

    def clean_password(self):
        return forms_clean_password(self.data['password'], self.data['password2'])