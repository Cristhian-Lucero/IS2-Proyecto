from django.shortcuts import render, redirect
from .forms import PublicacionForm  # Asegúrate de tener este formulario
from .models import Publicacion  # Asegúrate de que tienes el modelo Publicacion
from django.contrib.auth.decorators import login_required

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nueva_publicacion = form.save(commit=False)
            nueva_publicacion.autor = request.user
            nueva_publicacion.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm()

    # Apunta a 'crearpublicaciones/crearpublicaciones.html'
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
