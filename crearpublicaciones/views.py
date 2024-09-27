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
import json
from bs4 import BeautifulSoup
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

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
    # Obtener la publicación por su ID
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    
    # Renderizar la plantilla de previsualización
    return render(request, 'previsualizacion.html', {'publicacion': publicacion})

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

def parse_content(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    blocks = []
    
    for element in soup.contents:
        if element.name == 'p':
            blocks.append({'type': 'paragraph', 'content': element.text})
        elif element.name == 'h2':
            blocks.append({'type': 'heading', 'level': 'h2', 'content': element.text})
        elif element.name == 'h3':
            blocks.append({'type': 'heading', 'level': 'h3', 'content': element.text})
        elif element.name == 'blockquote':
            blocks.append({'type': 'quote', 'content': element.text})
        elif element.name == 'ul':
            items = [li.text for li in element.find_all('li')]
            blocks.append({'type': 'list', 'items': items})
        elif element.name == 'img':
            blocks.append({'type': 'image', 'src': element['src']})
        # Agrega más casos si es necesario

    return blocks


@login_required
# @check_permiso_publicacion_modificar(['crear contenido'])
def modificar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if request.method == 'GET':
        blocks = parse_content(publicacion.contenido_html)
        context = {
            'publicacion': publicacion,
            'blocks': blocks,
        }
        return render(request, 'modificarpublicacion.html', context)
    elif request.method == 'POST':
        data = json.loads(request.body)
        publicacion.titulo = data.get('title', publicacion.titulo)
        publicacion.contenido_html = data.get('contenido_html', publicacion.contenido_html)
        publicacion.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)


def split_content_into_blocks(content):
    bloques = []
    soup = BeautifulSoup(content, 'html.parser')
    
    # Extraer todos los párrafos, imágenes y listas como bloques separados
    for tag in soup.find_all(['p', 'img', 'ul', 'h2', 'h3']):
        if tag.name == 'p':
            bloques.append({'tipo': 'texto', 'contenido': tag.text})
        elif tag.name == 'img':
            bloques.append({'tipo': 'imagen', 'contenido': tag['src']})
        elif tag.name == 'ul':
            items = [li.get_text() for li in tag.find_all('li')]
            bloques.append({'tipo': 'viñetas', 'contenido': items})
        elif tag.name == 'h2':
            bloques.append({'tipo': 'heading2', 'contenido': tag.text})
        elif tag.name == 'h3':
            bloques.append({'tipo': 'heading3', 'contenido': tag.text})
    
    return bloques


@csrf_exempt
def modificar_publicacion_ajax(request, id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=id)

        try:
            data = json.loads(request.body)
            publicacion.titulo = data.get('title', publicacion.titulo)
            publicacion.contenido_html = data.get('content', publicacion.contenido_html)

            # Guardar los cambios en la publicación
            publicacion.save()

            return JsonResponse({'message': '¡Publicación actualizada con éxito!'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

    return JsonResponse({'message': 'Método no permitido.'}, status=405)



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
#@check_permiso_publicacion_modificar(['crear contenido'])
def personalizable(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    categoria = publicacion.categoria  # Obtener la categoría a partir de la relación con la publicación
    blocks = split_content_into_blocks(publicacion.contenido_html)  # Desglosar el contenido HTML en bloques

    return render(request, 'modificarpublicacion.html', {
        'publicacion': publicacion, 
        'blocks': blocks, 
        'categoria': categoria, 
        'publicacion_id': publicacion_id  
    })


@login_required
def guardar_publicacion_ajax(request, publicacion_id):
    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        data = json.loads(request.body)
        # Actualiza la publicación con los datos recibidos
        publicacion.titulo = data.get('title', publicacion.titulo)
        publicacion.contenido_html = data.get('contenido_html', publicacion.contenido_html)
        publicacion.save()
        return JsonResponse({'status': 'success'})


@csrf_exempt
def modificar_publicacion_ajax(request, id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            publicacion = Publicacion.objects.get(id=id)
            publicacion.titulo = data.get('title', publicacion.titulo)
            publicacion.contenido_html = data.get('content', publicacion.contenido_html)
            publicacion.categoria_id = data.get('categoria_id', publicacion.categoria_id)
            publicacion.save()
            return JsonResponse({'message': 'Publicación actualizada con éxito.'}, status=200)
        except Publicacion.DoesNotExist:
            return JsonResponse({'message': 'Publicación no encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
    return JsonResponse({'message': 'Método no permitido.'}, status=405)
