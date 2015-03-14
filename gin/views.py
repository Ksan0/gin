from django.contrib.auth import authenticate, login
from django.core.context_processors import csrf
from django.shortcuts import render
from subsystems.a_user.models import AUser


def createsuper(request):
    u = AUser.objects.create_user(password="1", is_superuser=True)
    u = authenticate(id=u.id, password="1")
    login(request, u)
    return render(request, "test.html")


def index(request):
    # a_user = User.objects.create_superuser(password="123")

    context = {}
    context.update(csrf(request))

    return render(request, "signup.html", context)


def main(request):
    return render(request, "main.html")


def page(request):
    return render(request, "page.html")


def dialog(request):
    return render(request, "dialog.html")


def paypal(request):
    return render(request, "paypal.html")


def test(request):
    #u = authenticate(id=1, password="1")
    #login(request, u)

    request.user.email_user(subject="ololo", message="alala")

    c = {
        "super": request.user.is_superuser
    }
    return render(request, "test.html", c)