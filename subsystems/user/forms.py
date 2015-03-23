from gin.forms import GinForm
from django import forms


class SignupForm(GinForm):
    email = forms.EmailField(widget=forms.EmailInput({"placeholder": "fff"}), label="Ваш email")
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__("ajax_signup_user", "POST", "", *args, **kwargs)

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError("Пароли не совпадают")
        return self.data['password']


class SigninForm(GinForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    
    def __init__(self, *args, **kwargs):
        super(SigninForm, self).__init__("ajax_signin_user", "POST", "", *args, **kwargs)