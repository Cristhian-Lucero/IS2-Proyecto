"""
Vistas de la aplicación login.

Define las vistas para la gestión de categorías, roles, y otras funcionalidades relacionadas
con la autenticación y administración de usuarios.
"""

from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *

from django.contrib.auth.decorators import login_required #para redirigir a login obligandolo a logearse
from django.contrib.auth import logout
# Create your views here.

def inicio(request):
    """
    Renderiza la página de inicio de sesión.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Renderiza la plantilla "login/inicio.html".
    """

    return render(request, "login/inicio.html")


def exit(request):
    """
    Cierra la sesión del usuario y redirige a la página de inicio.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Redirige a la vista "inicio" después de cerrar sesión.
    """

    logout(request)
    return redirect('inicio')

@login_required
def rol(request):
    """
    Renderiza la página de gestión de roles. Requiere que el usuario haya iniciado sesión.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/gestionRol.html".
    """

    return render(request, "rol/gestionRol.html")

def gestionarRol(request):
    """
    Renderiza la página de gestión de roles con la lista de categorías y roles.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/gestionRol.html" con categorías y roles.
    """

    x = list(Categoria.objects.all())
    y = list(Rol.objects.all())
    return render(request, 'rol/gestionRol.html', {
        'categorias': x,
        'roles': y
    })

def agregarRol(request):
    """
    Renderiza la página para agregar un rol y maneja la solicitud POST para guardar el nuevo rol.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/crudRol.html" o maneja la solicitud POST para guardar un nuevo rol.
    """

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
    """
    Elimina un rol específico basado en su ID y redirige a la página de adición de roles.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.
        rol_id (int): El ID del rol a eliminar.

    Retorna:
        HttpResponse: Redirige a 'adicionrol' después de eliminar el rol.
    """
    
    rol_seleccionado = get_object_or_404(Rol, id=rol_id)
    rol_seleccionado.delete()
    return redirect('adicionrol')

def editarRol(request, rol_id):
    """
    Renderiza la página para editar un rol y maneja la solicitud POST para actualizar los detalles del rol.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.
        rol_id (int): El ID del rol a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/editarRol.html' o actualiza el rol y redirige a 'adicionrol'.
    """
    
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
    """
    Renderiza la página de gestión de categorías y maneja las solicitudes POST para agregar una nueva categoría.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' con la lista de categorías o crea una nueva categoría.
    """

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
    """
    Elimina una categoría específica identificada por su ID y redirige a la página de gestión de categorías.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.
        categoria_id (int): El ID de la categoría a eliminar.

    Retorna:
        HttpResponse: Redirige a la vista 'gestioncategoria' después de eliminar la categoría.
    """

    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('gestioncategoria')

def editarCategoria(request, categoria_id):
    """
    Renderiza la página para editar una categoría y maneja la solicitud POST para actualizar los detalles de la categoría.

    Argumentos:
        request (HttpRequest): El objeto de la solicitud HTTP.
        categoria_id (int): El ID de la categoría a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' o actualiza la categoría y redirige a 'gestioncategoria'.
    """
    
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

   