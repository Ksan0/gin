from django.contrib.auth import login, authenticate
from django.core.validators import validate_email
from subsystems.a_user.models import AUser
from subsystems.utils.db import is_obj_exist, check_len
from subsystems.utils.json import render_to_json, AjaxPostErrors


def ajax_signup_user(request):
    """
        === INPUT ===
            method: POST
            "login": может быть email, телефонным номером или чем-то еще
            "password"
            "is_super": будет ли созданный юзер суперпользователем. Супера может создать только супер
        === OUTPUT ===
            status: AjaxError
            "user_id": если успешно, возвращает наш id
    """

    if request.method != "POST":
        return render_to_json(AjaxPostErrors.BAD_METHOD.json())

    try:
        form_login = check_len(request.POST.__getitem__("login"), 30)
        form_password = check_len(request.POST.__getitem__("password"), 30)
        form_password_confirm = check_len(request.POST.__getitem__("password_confirm"), 30)
        if form_password != form_password_confirm:
            return render_to_json(AjaxPostErrors.BAD_FORM.json())
        is_super = request.POST.get("is_super", False)
        if is_super and not request.user.is_superuser:
            return render_to_json(AjaxPostErrors.BAD_SESSION.json())
    except:
        return render_to_json(AjaxPostErrors.BAD_FORM.json())

    try:
        validate_email(form_login)
    except:
        return render_to_json(AjaxPostErrors.BAD_FORM.json())

    try:
        if is_obj_exist(AUser, email=form_login):
            return render_to_json(AjaxPostErrors.BAD_LOGIN_OR_PASSWORD.json())
        user = AUser.objects.create_user(email=form_login, password=form_password, is_superuser=is_super)
    except:
        return render_to_json(AjaxPostErrors.INTERNAL_ERROR.json())

    if not is_super:
        user = authenticate(id=user.id, password=form_password)
        login(request, user)

    response_data = {
        "user_id": user.id
    }
    response_data.update(AjaxPostErrors.NONE.json())

    return render_to_json(response_data)


def ajax_signin(request):
    """
        === INPUT ===
            method: POST
            "login": может быть email, телефонным номером или чем-то еще
            "password"
        === OUTPUT ===
            status: AjaxError
            "user_id": если успешно, то возвращает наш id
    """

    if request.method != "POST":
        return render_to_json(AjaxPostErrors.BAD_METHOD.json())

    try:
        form_login = check_len(request.POST.__getitem__("login"), 30)
        form_password = check_len(request.POST.__getitem__("password"), 30)
    except:
        return render_to_json(AjaxPostErrors.BAD_FORM.json())

    try:
        user = None

        if '@' in form_login:
            user = authenticate(email=form_login, password=form_password)
        elif 'a' == form_login[0]:
            user = authenticate(id=form_login[1:], password=form_password)

        if user is None:
            return render_to_json(AjaxPostErrors.BAD_LOGIN_OR_PASSWORD.json())
    except:
        return render_to_json(AjaxPostErrors.BAD_LOGIN_OR_PASSWORD.json())

    login(request, user)

    response_data = {
        "user_id": user.id
    }
    response_data.update(AjaxPostErrors.NONE.json())

    return render_to_json(response_data)
