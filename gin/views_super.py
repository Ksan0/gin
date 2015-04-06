from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from subsystems.a_user.models import AUser
from subsystems.operator.models import OperatorInfo


def view_super_init(request):
    email = request.GET['email']

    super_users_count = AUser.objects.filter(is_superuser=True).count()
    if super_users_count != 0:
        return redirect("/")
    AUser.objects.create_user(email=email, is_superuser=True)
    return redirect("/")