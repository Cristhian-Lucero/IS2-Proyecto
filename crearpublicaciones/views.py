from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render
from .models import Publicacion

# Create your views here.

def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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


def modificar_publicacion(request, pk):
    publicacion = Publicacion.objects.get(id=pk)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'crearPublicacion.html', {'form': form})


def eliminar_publicacion(request, pk):
    publicacion = Publicacion.objects.get(id=pk)
    publicacion.delete()
    return redirect('mis_publicaciones')

def arrastrar_soltarpagina(draganddrop.html')
