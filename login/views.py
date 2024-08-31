from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

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
    y = list(Rol.objects.all())
    return render(request, 'rol/gestionRol.html', {
        'categorias': x,
        'roles': y
    })

def agregarRol(request):
    x = list(Rol.objects.all())
    y = list(Permiso.objects.all())
    return render(request, 'rol/crudRol.html', {
        'roles': x,
        'permisos': y
    })

def gestionCategoria(request):
    if request.method == 'GET':
        #Si se entra desde el metodo GET 'visita la pagina'
        x = list(Categoria.objects.all())
        return render(request, 'rol/gestionCategoria.html', {
        'categorias': x,
        'form': CreateNewCategoria()
        })
    else:
        #Si se entra desde el metodo POST 'si se envia datos'
        Categoria.objects.create(
            descripcion_corta=request.POST['box_descripcion_corta'], 
            descripcion_larga=request.POST['box_descripcion_larga'], 
            estado=request.POST['box_estado']
        )
        return render(request, 'rol/gestionCategoria.html', {
            'categorias': list(Categoria.objects.all()),
            'form': CreateNewCategoria() 
        })

def eliminarCategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('gestioncategoria')
        
        
