from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required #para redirigir a login obligandolo a logearse
from django.contrib.auth import logout
# Create your views here.

def inicio(request):
    return render(request, "login/inicio.html")
@login_required
def base(request):
    return render(request, "login/base.html")
@login_required
def base2(request):
    return render(request, "login/base2.html")

def exit(request):
    logout(request)
    return redirect('inicio')

def gestionarRol(request):
    x = list(Categoria.objects.all())
    return render(request, 'rol/gestionRol.html', {
        'categorias': x
    })

def agregarRol(request):
    x = list(Rol.objects.all())
    y = list(Permiso.objects.all())
    return render(request, 'rol/crudRol.html', {
        'roles': x,
        'permisos': y
    })

def gestionCategoria(request):
    x = list(Rol.objects.all())
    y = list(Categoria.objects.all())
    z = list(Permiso.objects.all())
    return render(request, 'rol/gestionCategoria.html', {
        'roles': x,
        'categorias': y,
        'permisos': z
    })
