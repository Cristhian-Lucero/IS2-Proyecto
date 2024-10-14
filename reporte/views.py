from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import *
from login.models import *

# Create your views here.

@login_required
def masVistos(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas

    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.all()

    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    return render(request, 'masVistos.html', {'publicaciones': list(publicaciones.order_by('-vistas')), 'categorias': Categoria.objects.all()})