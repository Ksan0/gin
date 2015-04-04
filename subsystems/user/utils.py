from django import forms
from gin.settings import CustomSettings


def forms_clean_password(password, password2):
    if password != password2:
        raise forms.ValidationError("Пароли не совпадают")
    return password


def generate_restore_password_confirm_url(user):
    token = create_restore_password_token(user)
    return CustomSettings.DOMAIN_NAME_FULL + "/restore_password_confirm?uid={0}&token={1}".format(user.id, token)


def create_restore_password_token(user):
    to_hex = lambda x: "".join([hex(ord(c))[2:].zfill(2) for c in x])
    password_len_2 = int(len(user.password)/2)
    return to_hex(user.password[:password_len_2])