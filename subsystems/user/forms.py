from gin.forms import GinForm
from django import forms


def clean_password(password, password2):
    if password != password2:
        raise forms.ValidationError("Пароли не совпадают")
    return password


class SignupForm(GinForm):
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "fff"}), label="Ваш email")
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__("ajax_signup_user", "POST", "", "Зарегестрироваться", *args, **kwargs)

    def clean_password(self):
        return clean_password(self.data['password'], self.data['password2'])


class SigninForm(GinForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__("ajax_signin_user", "POST", "", "Войти", *args, **kwargs)


class RestorePasswordForm(GinForm):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(RestorePasswordForm, self).__init__("ajax_restore_password", "POST", "", "Восстановить", *args, **kwargs)


class RestorePasswordConfirmForm(GinForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    user_id = forms.IntegerField(widget=forms.HiddenInput(), label="")
    token = forms.CharField(widget=forms.HiddenInput(), label="")

    def __init__(self, *args, **kwargs):
        super(RestorePasswordConfirmForm, self).__init__("ajax_restore_password_confirm", "POST", "", "Сменить пароль", *args, **kwargs)

    def clean_password(self):
        return clean_password(self.data['password'], self.data['password2'])