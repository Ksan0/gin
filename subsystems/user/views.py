from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from subsystems.a_user.models import AUser
from subsystems.utils.ajax import AjaxResponseKeys
from subsystems.utils.json import render_to_json
from subsystems.user.forms import SignupForm, SigninForm, RestorePasswordForm, RestorePasswordConfirmForm
from subsystems.utils.user import create_restore_password_token


def ajax_signup(request):
    form = SignupForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_email = form.cleaned_data["email"]
        s_password = form.cleaned_data["password"]
        user = AUser.objects.create_user(s_email, s_password, False)
        user = authenticate(id=user.id, password=s_password)
        login(request, user)
    except:
        form.add_error("email", "Пользователь уже существует")
        return render_to_json(form.errors_to_json())

    return render_to_json({
        AjaxResponseKeys.REDIRECT: "/"
    })


def ajax_signin(request):
    form = SigninForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_email = form.cleaned_data["email"]
        s_password = form.cleaned_data["password"]
        user = AUser.objects.get(email=s_email)
        user = authenticate(id=user.id, password=s_password)
        if user is None:
            raise Exception()
        login(request, user)
    except:
        form.add_error(None, "Пользователь не существует или пароль неверный")
        return render_to_json(form.errors_to_json())

    return render_to_json({
        AjaxResponseKeys.REDIRECT: "/"
    })


def ajax_restore_password(request):
    form = RestorePasswordForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_email = form.cleaned_data["email"]
        user = AUser.objects.get(email=s_email)
        token = create_restore_password_token(user)
        restore_url = "http://localhost:8000/restore_password_confirm?uid={0}&token={1}".format(user.id, token)
        message = \
            "Это письмо пришло Вам, потому что кто-то нажал \"Восстановить пароль\" и ввел Ваш email\n" \
            "Если это сделали не Вы, просто проигнорируйте его\n" \
            "Для восстановления пароля перейдите по ссылке " + restore_url
        send_mail(subject="Восстановление пароля", message=message, from_email="db.testsystem@gmail.com", recipient_list=[user.email])
    except:
        pass

    return render_to_json({
        "message": "Письмо было отправленно на указанный email"
    })


def ajax_restore_password_confirm(request):
    form = RestorePasswordConfirmForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_user_id = form.cleaned_data['user_id']
        s_token = form.cleaned_data['token']

        user = AUser.objects.get(id=s_user_id)
        token = create_restore_password_token(user)

        if s_token != token:
            raise Exception("")

        s_password = form.cleaned_data['password']
        user.set_password(s_password)
        user.save()

        user = authenticate(id=user.id, password=s_password)
        login(request, user)
    except:
        form.add_error(None, "Вы используете устаревшую или неправильную ссылку")
        return render_to_json(form.errors_to_json())

    return render_to_json({})


def restore_password_confirm(request):
    context = {
        "restore_password_confirm_form": RestorePasswordConfirmForm(initial={
            'user_id': request.GET['uid'],
            'token': request.GET['token']
        })
    }

    return render(request, "restore_password_confirm.html", context)