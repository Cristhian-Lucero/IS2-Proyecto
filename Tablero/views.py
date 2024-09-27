from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import Publicacion

# Create your views here.
@login_required
def kanban_board(request):
    # Filtrar las publicaciones de acuerdo con los valores de estado de la base de datos
    borrador = Publicacion.objects.filter(estado='borrador')
    revision = Publicacion.objects.filter(estado='revision')
    publicado = Publicacion.objects.filter(estado='publicado')
    rechazado = Publicacion.objects.filter(estado='rechazado')

    context = {
        'borrador': borrador,
        'revision': revision,
        'publicado': publicado,
        'rechazado': rechazado,
    }
    return render(request, 'index.html', context)
