from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from subsystems.a_user.models import AUser
from subsystems.operator.models import OperatorInfo


def test_create(request):
    who = request.GET['who']

    if who == 'operator':
        i = len(OperatorInfo.objects.all())
        email = "o{0}@yo.ru".format(i)
        u = AUser.objects.create_user(email=email, password="1", is_operator=True, is_superuser=False)
        o = OperatorInfo.objects.create(user=u)
        u = authenticate(id=u.id, password="1")
        login(request, u)
    elif who == 'super':
        i = len(AUser.objects.all())
        email = "a{0}@yo.ru".format(i)
        u = AUser.objects.create_user(email=email, password="1", is_superuser=True)
        u = authenticate(id=u.id, password="1")
        login(request, u)

    return redirect("/")