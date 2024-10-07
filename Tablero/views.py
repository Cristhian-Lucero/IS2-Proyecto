from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import Publicacion
from login.models import Categoria, UsuarioRolCategoria, Permiso
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # Asegúrate de importar csrf_exempt
import json
from login.utils import *

@login_required
def kanban_board(request, categoria_id=None):
    """
    View para mostrar el tablero Kanban con publicaciones organizadas por estado.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        categoria_id (int, opcional): El ID de la categoría seleccionada. Si no se proporciona, se selecciona la primera categoría activa.

    Returns:
        HttpResponse: Renderiza la plantilla 'index.html' con el contexto que incluye las publicaciones en diferentes estados y las categorías activas.
    """

    if not verificar_permisos_categoria_id(request, ['rechazar contenido', 'publicar contenido', 'cambiar estado publicacion'], categoria_id):
        return render(request, 'sin_permiso.html')
    # Obtener el usuario actual
    usuario_actual = request.user

    # Obtener los roles del usuario
    roles_usuario = UsuarioRolCategoria.objects.filter(usuario_id=usuario_actual.id).values_list('rol_id', flat=True)

    # Obtener los permisos 11, 12 o 13
    permisos_requeridos = Permiso.objects.filter(id__in=[11, 12, 13])

    # Filtrar las categorías que están asociadas con los roles que tienen los permisos 11, 12 o 13
    categorias_usuario = Categoria.objects.filter(
        usuariorolcategoria__rol__in=roles_usuario, 
        usuariorolcategoria__rol__permisos__in=permisos_requeridos,
        estado='Activo'
    ).distinct()

    # Si no se especifica una categoría, seleccionamos la primera categoría activa
    if request.GET.get('categoria_id'):
        categoria_id = request.GET.get('categoria_id')

    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id, estado='Activo')
    else:
        # Selecciona automáticamente la primera categoría activa si no se especifica ninguna
        categoria = categorias_usuario.first()

    # Asegúrate de que siempre haya una categoría válida
    if not categoria:
        categoria = categorias_usuario.first()

    # Filtrar publicaciones por estado y categoría seleccionadaaaa
    borrador = Publicacion.objects.filter(estado='borrador', categoria=categoria)
    revision = Publicacion.objects.filter(estado='revision', categoria=categoria)
    publicado = Publicacion.objects.filter(estado='publicado', categoria=categoria)
    rechazado = Publicacion.objects.filter(estado='rechazado', categoria=categoria)

    context = {
        'categoria': categoria,  # La categoría seleccionada o la primera por defecto
        'borrador': borrador,
        'revision': revision,
        'publicado': publicado,
        'rechazado': rechazado,
        'categorias_activas': categorias_usuario,  # Solo las categorías permitidas para el usuario
    }

    return render(request, 'index.html', context)

# Vista para actualizar el estado de una tarea
@csrf_exempt  # Decorador para eximir esta vista de la protección CSRF
@login_required
def update_task_state(request, task_id):
    """
    View para actualizar el estado de una publicación.

    Args:
        request (HttpRequest): El objeto de solicitud HTTP.
        task_id (int): El ID de la publicación a actualizar.

    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """

    if request.method == 'POST':
        try:
            # Obtener el nuevo estado desde el cuerpo de la solicitud
            data = json.loads(request.body)
            new_state = data.get('estado')
            
            # Obtener la publicación y actualizar su estado
            publicacion = get_object_or_404(Publicacion, id=task_id)
            publicacion.estado = new_state
            publicacion.save()

            return JsonResponse({"message": "Estado actualizado correctamente"}, status=200)
        except Publicacion.DoesNotExist:
            return JsonResponse({"error": "Publicación no encontrada"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido"}, status=405)
