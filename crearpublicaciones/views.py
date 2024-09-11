from django.shortcuts import render
from .forms import PublicacionForm  
from .models import Publicacion  
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
import time

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.user = request.user  # Asigna el usuario autenticado
            publicacion.save()  # Guarda la publicación
            time.sleep(1)
            return redirect('mis_publicaciones')  # Redirige a la página "Mis Publicaciones"
    else:
        form = PublicacionForm()
    
    return render(request, 'crearpublicacion.html', {'form': form})



def previsualizar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, id=pk)
    return render(request, 'previsualizacion.html', {'publicacion': publicacion, 'user': publicacion.user})

@login_required
def mis_publicaciones(request):
    # Obtén todas las publicaciones del usuario autenticado
    publicaciones = Publicacion.objects.filter(user=request.user)

    return render(request, 'misPublicaciones.html', {'publicaciones': publicaciones})

@login_required
def modificar_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, id=publicacion_id)

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')  # Redirige a la lista de publicaciones después de guardar
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

@login_required
def personalizable(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', 'Título por defecto')
        texto_corto = request.POST.get('texto_corto', 'Texto corto por defecto')
        
        # Crea y guarda la publicación
        publicacion = Publicacion(
            titulo=titulo,
            texto_corto=texto_corto,
            user=request.user,  
        )
        publicacion.save()

        # Espera 1 seg antes de redirigir 
        time.sleep(1)

        # Redirige a "Mis Publicaciones"
        return redirect('misPublicaciones')
    
    return render(request, 'personalizable.html')
