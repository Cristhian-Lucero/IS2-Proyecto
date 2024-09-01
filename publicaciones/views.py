from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Publicacion
from .forms import PublicacionForm

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.estado = 'borrador'
            publicacion.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm()
    return render(request, 'publicaciones/crear_publicacion.html', {'form': form})

@login_required
def modificar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'publicaciones/crear_publicacion.html', {'form': form, 'modificar': True})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    publicacion.delete()
    return redirect('mis_publicaciones')

@login_required
def previsualizacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, usuario=request.user)
    return render(request, 'publicaciones/previsualizacion.html', {'publicacion': publicacion})

@login_required
def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(usuario=request.user)
    return render(request, 'publicaciones/mis_publicaciones.html', {'publicaciones': publicaciones})


# Create your views here.
from django.shortcuts import render, redirect
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.usuario = request.user
            publicacion.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm()
    return render(request, 'publicaciones/crear_publicacion.html', {'form': form})

@login_required
def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(usuario=request.user)
    return render(request, 'publicaciones/mis_publicaciones.html', {'publicaciones': publicaciones})
