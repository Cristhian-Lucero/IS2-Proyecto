from django.shortcuts import render
from django.contrib.auth.decorators import login_required #genera la necesidad de logearse para poder ingresar a una vista

# Create your views here.

def inicio(request):
    return render(request, "login/inicio.html")
@login_required
def base(request):
    return render(request, "login/base.html")
@login_required
def base2(request):
    return render(request, "login/base2.html")