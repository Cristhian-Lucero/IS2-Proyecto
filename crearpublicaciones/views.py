"""
Vistas de la aplicación 'crearpublicaciones'.

Este archivo define las vistas para manejar la creación, modificación,
previsualización, y eliminación de publicaciones, así como la selección
de plantillas y la personalización de las publicaciones.
"""
from login.utils import *
from django.shortcuts import render
from .forms import *
from .models import *
from login.models import Categoria
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from utils.decorators import *
import time
import json
from bs4 import BeautifulSoup
from django.http import JsonResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from login.utils import *

@login_required
def crear_publicacion(request, categoria_id):
    """
    Vista para crear una nueva publicación.

    Si se envía una solicitud POST, se procesa el formulario de la publicación
    y se guarda la nueva publicación asociada al usuario autenticado.
    Luego, redirige a la página 'Mis Publicaciones'. Si es una solicitud GET,
    se muestra el formulario vacío para crear una nueva publicación.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        categoria_id (int): ID de la categoría a la cual pertenece la publicación.

    Returns:
        HttpResponse: Renderiza la página de creación de publicaciones o
        redirige a 'mis_publicaciones' después de guardar.
    """

    if not verificar_permisos_categoria_id(request, ['crear contenido'], categoria_id):
        return render(request, 'sin_permiso.html')

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.user = request.user  # Asigna el usuario autenticado
            publicacion.categoria = Categoria.objects.get(id=categoria_id)
            publicacion.fecha_publicacion = null
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
    Vista para previsualizar una publicación existente.

    Muestra la publicación y sus comentarios asociados, y permite saber si el usuario ha dado "Me gusta".

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación a previsualizar.

    Returns:
        HttpResponse: Renderiza la plantilla de previsualización con la publicación y sus datos.
    """
    
    # Obtener la publicación por su ID
    try:
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)

        if (request.user != publicacion.user and publicacion.estado != 'publicado') or publicacion.categoria.estado == 'Inactivo':
            print('aprobao')
            if not verificar_permisos_categoria_id(request, ['aprobar contenido', 'rechazar contenido', 'publicar contenido', 'cambiar estado publicacion', 'visualizar historial cambios', 'gestionar contenido otros'], publicacion.categoria_id):
                return render(request, 'publicacion_no_disponible.html')

        comentarios = Comentario.objects.filter(publicacion=publicacion_id)
        #publicacion.vistas += 1
        #publicacion.save()
        likeado = Likes.objects.filter(user=request.user, publicacion=publicacion_id).exists()
        # Renderizar la plantilla de previsualización
        

        return render(request, 'previsualizacion.html', {
            'publicacion': publicacion,
            'comentarios': comentarios,
            'likeado': likeado
            })
    except Http404:
        # Renderiza un HTML específico si la publicación no existe
        return render(request, 'publicacion_no_existe.html')

@csrf_exempt
def incrementar_vistas(request, publicacion_id):
    """
    Vista para incrementar el contador de vistas de una publicación.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación.

    Returns:
        JsonResponse: Respuesta en formato JSON con el resultado de la operación.
    """

    if request.method == 'POST':
        try:
            publicacion = get_object_or_404(Publicacion, id=publicacion_id)
            publicacion.vistas += 1
            publicacion.save()
            return JsonResponse({'status': 'success', 'vistas': publicacion.vistas})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

@login_required
def likear(request, publicacion_id):
    """
    Vista para dar "Me gusta" a una publicación.

    Permite que el usuario autenticado agregue un "Me gusta" a la publicación especificada.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación.

    Returns:
        HttpResponse: Redirige a la previsualización de la publicación.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if not verificar_permisos_categoria_id(request, ['interactuar publicaciones'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')

    likeado = Likes.objects.filter(user=request.user, publicacion=publicacion_id).exists()
    if not likeado:
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        nuevo_like = Likes(user=request.user, publicacion=publicacion)
        nuevo_like.save()
        publicacion.me_gustas += 1
        publicacion.save()
    return redirect('previsualizar_publicacion', publicacion_id=publicacion_id)

@login_required
def dislikear(request, publicacion_id):
    """
    Vista para quitar un "Me gusta" de una publicación.

    Permite que el usuario autenticado quite un "Me gusta" de la publicación especificada.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación.

    Returns:
        HttpResponse: Redirige a la previsualización de la publicación.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if not verificar_permisos_categoria_id(request, ['interactuar publicaciones'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')

    likeado = Likes.objects.filter(user=request.user, publicacion=publicacion_id).exists()
    like = Likes.objects.filter(user=request.user, publicacion=publicacion_id)
    if likeado:
        like.delete()
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        publicacion.me_gustas -= 1
        publicacion.save()
    return redirect('previsualizar_publicacion', publicacion_id=publicacion_id)

@login_required
def mis_publicaciones(request):
    """
    Vista para mostrar las publicaciones del usuario autenticado.

    Recupera todas las publicaciones creadas por el usuario actual y las muestra
    en la página 'Mis Publicaciones'.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.

    Returns:
        HttpResponse: Renderiza la página 'Mis Publicaciones' con todas las publicaciones del usuario.
    """

    publicaciones = Publicacion.objects.filter(user=request.user)
    return render(request, 'misPublicaciones.html', {'publicaciones': publicaciones})

@login_required
def gestionPublicacionOtros(request, categoria_id):
    """
    Vista para gestionar las publicaciones de otros usuarios dentro de una categoría.

    Permite al usuario autenticado visualizar todas las publicaciones en una categoría
    específica si tiene los permisos adecuados.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        categoria_id (int): ID de la categoría.

    Returns:
        HttpResponse: Renderiza la página de gestión de publicaciones de terceros.
    """

    if not verificar_permisos_categoria_id(request, ['gestionar contenido otros'], categoria_id):
        return render(request, 'sin_permiso.html')

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
def modificar_publicacion(request, publicacion_id):
    """
    Vista para modificar una publicación existente.

    Permite editar el título y contenido de una publicación. Muestra el formulario con
    el contenido existente si la solicitud es GET, y guarda los cambios si es POST.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación a modificar.

    Returns:
        HttpResponse: Renderiza la página de modificación o devuelve un JsonResponse con el estado.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if not verificar_permisos_categoria_id(request, ['crear contenido'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')
    
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

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación que se desea eliminar.

    Returns:
        HttpResponse: Renderiza la página de confirmación de eliminación o redirige tras eliminar.
    """
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if not verificar_permisos_categoria_id(request, ['crear contenido'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')

    if request.method == 'POST':
        publicacion.delete()
        return redirect('home')
    return render(request, 'eliminarpublicacion.html', {'publicacion': publicacion})

@login_required
def eliminar_publicacion_otros(request, publicacion_id):
    """
    Vista para eliminar una publicación de un tercero.

    Busca una publicación por su ID y la elimina si la solicitud es POST.
    Luego, redirige a 'Gestion de publicaciones'.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación que se desea eliminar.

    Returns:
        HttpResponse: Renderiza la página de confirmación de eliminación o redirige tras eliminar.
    """

    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if not verificar_permisos_categoria_id(request, ['gestionar contenido otros'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')
    
    if request.method == 'POST':
        publicacion.delete()
        return redirect('home')
    return render(request, 'eliminarpublicacion.html', {'publicacion': publicacion})

@login_required
def seleccionar_plantilla(request, categoria_id):
    """
    Vista para seleccionar una plantilla para la publicación.

    Muestra las opciones de plantillas disponibles para ser usadas
    en la creación de publicaciones.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        categoria_id (int): ID de la categoría de la publicación.

    Returns:
        HttpResponse: Renderiza la página de selección de plantillas.
    """

    if not verificar_permisos_categoria_id(request, ['crear contenido'], categoria_id):
        return render(request, 'sin_permiso.html')

    return render(request, 'seleccionar_plantilla.html', {
        'categoria_id': categoria_id
    })


@login_required
def personalizable(request, categoria_id):
    """
    Vista para crear una nueva publicación en modo borrador o reutilizar una existente.

    Permite al usuario personalizar una publicación existente o crear una nueva en modo borrador.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        categoria_id (int): ID de la categoría a la que pertenece la publicación.

    Returns:
        HttpResponse: Renderiza la página de personalización de publicaciones.
    """

    # Obtener la categoría
    categoria = get_object_or_404(Categoria, id=categoria_id)

    if not verificar_permisos_categoria_id(request, ['crear contenido'], categoria_id):
        return render(request, 'sin_permiso.html')

    # Crear una nueva publicación en borrador o reutilizar una existente
    publicacion, created = Publicacion.objects.get_or_create(
        user=request.user,
        categoria=categoria,
        estado='borrador',
        defaults={'titulo': '', 'contenido_html': ''}
    )

    blocks = split_content_into_blocks(publicacion.contenido_html) if publicacion.contenido_html else []

    return render(request, 'personalizable.html', {
        'publicacion': publicacion,
        'blocks': blocks,
        'categoria': categoria,
        'publicacion_id': publicacion.id,
    })


@login_required
def guardar_publicacion_ajax(request, publicacion_id):
    """
    Vista para guardar una publicación mediante una solicitud AJAX.

    Permite actualizar el título y contenido de una publicación utilizando una solicitud POST.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación a guardar.

    Returns:
        JsonResponse: Respuesta en formato JSON con el estado de la operación.
    """

    if request.method == 'POST':
        publicacion = get_object_or_404(Publicacion, id=publicacion_id)
        data = json.loads(request.body)
        publicacion.titulo = data.get('title', publicacion.titulo)
        publicacion.contenido_html = data.get('content', publicacion.contenido_html)
        publicacion.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)

@login_required
def comentario(request, publicacion_id):
    """
    Vista para agregar un comentario a una publicación.

    Permite al usuario autenticado agregar un comentario a la publicación especificada.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        publicacion_id (int): ID de la publicación a comentar.

    Returns:
        HttpResponse: Renderiza la página de comentarios o redirige tras agregar el comentario.
    """

    # Obtener la publicación en base al id
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)
    if not verificar_permisos_categoria_id(request, ['interactuar publicaciones'], publicacion.categoria_id):
        return render(request, 'sin_permiso.html')
    ##
    # Si el formulario ha sido enviado
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.user = request.user
            comentario.publicacion = publicacion  # Asignar el comentario a la publicación
            comentario.save()
            # Redireccionar después de guardar el comentario (opcional)
            return redirect(f"{reverse('previsualizar_publicacion', args=[publicacion_id])}#comentario_{comentario.id}")
    else:
        form = ComentarioForm()

    # Renderizar el template y pasar el formulario y la publicación al contexto
    return render(request, 'comentar.html', {
        'form': form, 
        'publicacion': publicacion
        })

@login_required
def eliminar_comentario(request, comentario_id):
    """
    Vista para eliminar un comentario de una publicación.

    Permite al usuario autenticado eliminar su propio comentario o un comentario de terceros si tiene permisos.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        comentario_id (int): ID del comentario a eliminar.

    Returns:
        HttpResponse: Redirige a la previsualización de la publicación tras eliminar el comentario.
    """

    comentario = get_object_or_404(Comentario, id=comentario_id)

    publicacion = get_object_or_404(Publicacion, id=comentario.publicacion_id)
    if(comentario.user_id != request.user.id):
        if not verificar_permisos_categoria_id(request, ['gestionar contenido otros'], publicacion.categoria_id):
            return render(request, 'sin_permiso.html')
    
    if request.method == 'POST':
        comentario.delete()
        return redirect('previsualizar_publicacion', publicacion_id=comentario.publicacion.id)
    
@csrf_exempt
def modificar_publicacion_ajax(request, id):
    """
    Vista para modificar una publicación existente mediante una solicitud AJAX.

    Permite actualizar el título, contenido y categoría de una publicación.

    Args:
        request (HttpRequest): La solicitud HTTP recibida.
        id (int): ID de la publicación a modificar.

    Returns:
        JsonResponse: Respuesta en formato JSON con el estado de la operación.
    """

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
