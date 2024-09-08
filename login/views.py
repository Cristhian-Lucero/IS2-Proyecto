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

def rol(request):
    return render(request, "rol/gestionRol.html")

def gestionarRol(request):
    x = list(Categoria.objects.all())
    y = list(Rol.objects.all())
    return render(request, 'rol/gestionRol.html', {
        'categorias': x,
        'roles': y
    })

def agregarRol(request):
    x = list((Rol.objects.all()).order_by('id'))
    y = list(Permiso.objects.all())
    if request.method == 'GET':
        return render(request, 'rol/crudRol.html', {
            'roles': x,
            'permisos': y,
            'form': CreateNewRol()
        })
    else:
        permisos_seleccionados = request.POST.getlist('permisos')
        nuevo_rol = Rol.objects.create(nombre=request.POST['box_nombre'], descripcion=request.POST['box_descripcion'])
        nuevo_rol.permisos.set(permisos_seleccionados)
        nuevo_rol.save()
        return redirect('adicionrol')

def eliminarRol(request, rol_id):
    rol_seleccionado = get_object_or_404(Rol, id=rol_id)
    rol_seleccionado.delete()
    return redirect('adicionrol')

def editarRol(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)

    if request.method == 'POST':
        form = CreateNewRol(request.POST)
        if form.is_valid():
            rol.nombre = form.cleaned_data['box_nombre']
            rol.descripcion = form.cleaned_data['box_descripcion']

            permisos_seleccionados = request.POST.getlist('permisos')

            rol.permisos.set(permisos_seleccionados)
            rol.save()
            return redirect('adicionrol')
    else:
        
        form = CreateNewRol(initial={
            'box_nombre': rol.nombre,
            'box_descripcion': rol.descripcion,
            'permisos': list(rol.permisos.all().values_list('id', flat=True))
        })
    

    return render(request, 'rol/editarRol.html', {
        'rol': rol,
        'form': form
    })


def gestionCategoria(request):
    if request.method == 'GET':
        #Si se entra desde el metodo GET 'visita la pagina'
        x = list((Categoria.objects.all()).order_by('id'))
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

def editarCategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CreateNewCategoria(request.POST)
        if form.is_valid():
            categoria.descripcion_corta = form.cleaned_data['box_descripcion_corta']
            categoria.descripcion_larga = form.cleaned_data['box_descripcion_larga']
            categoria.estado = form.cleaned_data['box_estado']
            categoria.save()
            return redirect('gestioncategoria')
    else:
        form = CreateNewCategoria(initial={
            'box_descripcion_corta': categoria.descripcion_corta,
            'box_descripcion_larga': categoria.descripcion_larga,
            'box_estado': categoria.estado
        })

    return render(request, 'rol/editarCategoria.html', {
        'form': form,
        'categoria': categoria
    })

@login_required
def seleccionar_plantilla(request):
    return render(request, 'ruta/a/tu/template_seleccionar_plantilla.html')
   