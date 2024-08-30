from django.shortcuts import render
from django.contrib.auth.decorators import login_required #para redirigir a login obligandolo a logearse

# Create your views here.

def inicio(request):
    return render(request, "login/inicio.html")
@login_required
def base(request):
    return render(request, "login/base.html")
@login_required
def base2(request):
    return render(request, "login/base2.html")