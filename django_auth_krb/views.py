from django.contrib.auth.views import login, logout_then_login
from django.shortcuts import redirect
from django.conf import settings


def krb_login(request):
    if request.user.is_authenticated():
        redirect_url = request.GET.get('next') or settings.LOGIN_REDIRECT_URL
        return redirect(redirect_url)
    else:
        return login(request)


def krb_logout(request):
    return logout_then_login(request)
