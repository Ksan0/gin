from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from .settings_local import SettingsLocal
from subsystems.a_user.models import AUser
from subsystems.operator.models import OperatorInfo


def view_create(request):
    if not SettingsLocal.DEBUG:
        return redirect("/")

    who = request.GET['who']

    if who == 'operator':
        i = OperatorInfo.objects.count()
        u = AUser.objects.create_user("o{0}@yo.ru".format(i), password="1", is_operator=True)
        OperatorInfo.objects.create(user=u)
        u = authenticate(id=u.id, password="1")
        login(request, u)

    return redirect("/")
