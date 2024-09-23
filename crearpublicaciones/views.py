"""
Vistas de la aplicación 'crearpublicaciones'.

Este archivo define las vistas para manejar la creación, modificación,
previsualización, y eliminación de publicaciones, así como la selección
de plantillas y la personalización de las publicaciones.
"""

from django.shortcuts import render
from .forms import PublicacionForm
from .models import Publicacion
from login.models import Categoria
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from utils.decorators import *
import time
from django.http import JsonResponse
from django.shortcuts import redirect

@login_required
# @check_permiso_categoria(['crear contenido'])
def crear_publicacion(request, categoria_id):
    """
    Vista para crear una nueva publicación.

    Si se envía una solicitud POST, se procesa el formulario de la publicación
    y se guarda la nueva publicación asociada al usuario autenticado.
    Luego, redirige a la página 'Mis Publicaciones'. Si es una solicitud GET,
    se muestra el formulario vacío para crear una nueva publicación.

    Returns:
        HttpResponse: Renderiza la página de creación de publicaciones o
        redirige a 'mis_publicaciones' después de guardar.
    """

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.user = request.user  # Asigna el usuario autenticado
            publicacion.categoria = Categoria.objects.get(id=categoria_id)
            publicacion.save()  # Guarda la publicación
            time.sleep(1)
            return redirect('mis_publicaciones')  # Redirige a la página "Mis Publicaciones"
    else:
        form = PublicacionForm()

    return render(request, 'crearpublicacion.html', {
        'form': form,
        'categoria_id': categoria_id
        })


@login_required
def previsualizar_publicacion(request, publicacion_id):
    """
    Vista para previsualizar una publicación.

    Busca una publicación por su clave primaria (publicacion_id) y la muestra en una página
    de previsualización.

    Argumentos:
        publicacion_id (int): Clave primaria de la publicación a previsualizar.

    Returns:
        HttpResponse: Renderiza la página de previsualización con los datos de la publicación.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    return render(request, 'previsualizacion.html', {'publicacion': publicacion, 'user': publicacion.user})

@login_required
def mis_publicaciones(request):
    """
    Vista para mostrar las publicaciones del usuario autenticado.

    Recupera todas las publicaciones creadas por el usuario actual y las muestra
    en la página 'Mis Publicaciones'.

    Returns:
        HttpResponse: Renderiza la página 'Mis Publicaciones' con todas las publicaciones del usuario.
    """

    publicaciones = Publicacion.objects.filter(user=request.user)

    return render(request, 'misPublicaciones.html', {'publicaciones': publicaciones})


@login_required

@check_permiso_categoria(['gestionar contenido otros'])
def gestionPublicacionOtros(request, categoria_id):

    publicaciones_gestionables = Publicacion.objects.filter(categoria=categoria_id)

    return render(request, 'GestionPublicaciones3ros.html', {
        'publicaciones': publicaciones_gestionables,
        'categoria_nombre': get_object_or_404(Categoria, id=categoria_id).descripcion_corta
        })

@login_required
# @check_permiso_publicacion_modificar(['crear contenido'])
def modificar_publicacion(request, publicacion_id):
    """
    Vista para modificar una publicación existente.

    Permite al usuario editar una publicación específica. Si es una solicitud
    POST, actualiza la publicación y redirige a 'Mis Publicaciones'. Si es una solicitud GET,
    muestra el formulario con los datos de la publicación existente.

    Argumentos:
        publicacion_id (int): ID de la publicación que se desea modificar.

    Returns:
        HttpResponse: Renderiza la página de modificación o redirige después de guardar.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')  # Redirige a la lista de publicaciones después de guardar
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'modificarpublicacion.html', {'form': form})


@login_required
# @check_permiso_publicacion_modificar(['crear contenido'])
def eliminar_publicacion(request, publicacion_id):
    """
    Vista para eliminar una publicación.

    Busca una publicación por su ID y la elimina si la solicitud es POST.
    Luego, redirige a 'Mis Publicaciones'.

    Argumentos:
        publicacion_id (int): ID de la publicación que se desea eliminar.

    Returns:
        HttpResponse: Renderiza la página de confirmación de eliminación o redirige tras eliminar.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if request.method == 'POST':
        publicacion.delete()
        return redirect('mis_publicaciones')
    return render(request, 'eliminarpublicacion.html', {'publicacion': publicacion})


@login_required
# @check_permiso_categoria(['crear contenido'])
def seleccionar_plantilla(request, categoria_id):
    """
    Vista para seleccionar una plantilla para la publicación.

    Muestra las opciones de plantillas disponibles para ser usadas
    en la creación de publicaciones.

    Returns:
        HttpResponse: Renderiza la página de selección de plantillas.
    """

    return render(request, 'seleccionar_plantilla.html', {
        'categoria_id': categoria_id
    })


@login_required
# @check_permiso_publicacion_modificar(['crear contenido'])
def personalizable(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    return render(request, 'personalizable.html', {
        'categoria': categoria
    })


@login_required
def guardar_publicacion_ajax(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        titulo = data.get('title')
        contenido_html = data.get('content')
        categoria_id = data.get('categoria_id')

        # Buscar la categoría por ID
        categoria = Categoria.objects.get(id=categoria_id)

        # Crear la nueva publicación con estado 'borrador' por defecto
        nueva_publicacion = Publicacion(
            titulo=titulo,
            contenido_html=contenido_html,
            estado='borrador',  # Estado por defecto
            user=request.user,
            categoria=categoria
        )
        nueva_publicacion.save()

        # Devolver una respuesta JSON de éxito
        return JsonResponse({'success': True})

    return JsonResponse({'error': 'Invalid request'}, status=400)
