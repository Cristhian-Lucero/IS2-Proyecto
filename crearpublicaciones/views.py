from django.shortcuts import render, get_object_or_404, redirect
from .forms import PublicacionForm
from .models import Publicacion

# Vistas para la aplicación

def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)  # No guardes aún en la base de datos
            publicacion.user = request.user  # Asigna el usuario autenticado
            publicacion.save()  # Guarda la publicación con el usuario asignado
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm()
    
    return render(request, 'crearpublicacion.html', {'form': form})

def previsualizar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, id=pk)
    return render(request, 'previsualizacion.html', {'publicacion': publicacion, 'user': publicacion.user})

def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(user=request.user)  
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

def seleccionar_plantilla(request):
    return render(request, 'seleccionar_plantilla.html')

def personalizable(request):
    return render(request, 'personalizable.html')
