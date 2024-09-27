from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import Publicacion
from login.models import Categoria
from django.shortcuts import render, get_object_or_404

# Create your views here.
@login_required
def kanban_board(request, categoria_id=None):
    # Si no se especifica una categoría, seleccionamos la primera categoría activa por defecto
    if request.GET.get('categoria_id'):
        categoria_id = request.GET.get('categoria_id')
    
    if categoria_id:
        categoria = get_object_or_404(Categoria, id=categoria_id, estado='Activo')
    else:
        # Selecciona automáticamente la primera categoría activa si no se especifica ninguna
        categoria = Categoria.objects.filter(estado='Activo').first()
    
    # Filtrar publicaciones por estado y categoría seleccionada
    borrador = Publicacion.objects.filter(estado='borrador', categoria=categoria)
    revision = Publicacion.objects.filter(estado='revision', categoria=categoria)
    publicado = Publicacion.objects.filter(estado='publicado', categoria=categoria)
    rechazado = Publicacion.objects.filter(estado='rechazado', categoria=categoria)

    # Obtener todas las categorías activas para el menú desplegable
    categorias_activas = Categoria.objects.filter(estado='Activo')

    context = {
        'categoria': categoria,  # La categoría seleccionada o la primera por defecto
        'borrador': borrador,
        'revision': revision,
        'publicado': publicado,
        'rechazado': rechazado,
        'categorias_activas': categorias_activas,  # Todas las categorías activas para el menú
    }
    
    return render(request, 'index.html', context)

