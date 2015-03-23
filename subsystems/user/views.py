from django.contrib.auth import authenticate, login
from subsystems.a_user.models import AUser
from subsystems.utils.ajax import AjaxResponseKeys
from subsystems.utils.json import render_to_json
from subsystems.user.forms import SignupForm, SigninForm


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
        user = AUser.objects.get(s_email, s_password, False)
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