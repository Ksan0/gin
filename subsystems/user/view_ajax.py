from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from subsystems.a_user.models import AUser
from subsystems.user.forms import SignupForm, SigninForm, RestorePasswordRequestForm, RestorePasswordConfirmForm
from subsystems.user.utils import generate_restore_password_confirm_url
from subsystems.utils.ajax import AjaxResponseKeys
from subsystems.utils.json import render_to_json


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


def ajax_restore_password_request(request):
    form = RestorePasswordRequestForm(request.POST or None)

    if request.method != "POST":
        form.add_error(None, "bad method")
        return render_to_json(form.errors_to_json())

    if not form.is_valid():
        return render_to_json(form.errors_to_json())

    try:
        s_email = form.cleaned_data["email"]
        user = AUser.objects.get(email=s_email)
        restore_url = generate_restore_password_confirm_url(user)
        message = \
            "Это письмо пришло Вам, потому что кто-то нажал \"Восстановить пароль\" и ввел Ваш email\n" \
            "Если это сделали не Вы, просто проигнорируйте его\n" \
            "Для восстановления пароля перейдите по ссылке:\n" + restore_url
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