from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .forms import PublicacionForm
from .models import Publicacion

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion
from .forms import PublicacionForm

def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save()  # Guarda la publicación
            # Redirige automáticamente a la página de Mis Publicaciones
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm()
    
    return render(request, 'crearpublicacion.html', {'form': form})



def previsualizar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, id=pk)
    return render(request, 'previsualizacion.html', {'publicacion': publicacion, 'user': publicacion.user})



def mis_publicaciones(request):
    publicaciones = Publicacion.objects.all()  # Solo las publicaciones del usuario
    return render(request, 'misPublicaciones.html', {'publicaciones': publicaciones})


def modificar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, id=id)
    
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    
    return render(request, 'modificarpublicacion.html', {'form': form})


def eliminar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, id=id)
    
    if request.method == 'POST':
        publicacion.delete()
        return redirect('mis_publicaciones')
    
    return render(request, 'eliminarpublicacion.html', {'publicacion': publicacion})