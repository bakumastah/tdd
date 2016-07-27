from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse


def persona_login(request):
    user = authenticate(assertion=request.POST['assertion'])
    if user:
        auth_login(request, user)
    return HttpResponse('OK')
