from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required

@login_required
def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(autor=request.user)
    return render(request, 'mis_publicaciones.html', {'publicaciones': publicaciones})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Publicacion
from .forms import PublicacionForm
from django.contrib.auth.decorators import login_required

@login_required
def crear_publicacion(request, pk=None):
    if pk:
        publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
    else:
        publicacion = None

    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect('previsualizacion', pk=publicacion.pk)
    else:
        form = PublicacionForm(instance=publicacion)

    return render(request, 'crear_publicacion.html', {'form': form})



@login_required
def previsualizacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        return redirect('mis_publicaciones')
    return render(request, 'previsualizacion.html', {'publicacion': publicacion})

@login_required
def previsualizacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'previsualizacion.html', {'publicacion': publicacion})

@login_required
def mis_publicaciones(request):
    publicaciones = Publicacion.objects.filter(autor=request.user)
    return render(request, 'mis_publicaciones.html', {'publicaciones': publicaciones})


@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            # Manejo manual de los datos del formulario
            encabezado = form.cleaned_data['encabezado']
            cuerpo = form.cleaned_data['cuerpo']
            imagen = form.cleaned_data['imagen']
            
            # Crear la publicación manualmente
            publicacion = Publicacion(
                autor=request.user,
                encabezado=encabezado,
                cuerpo=cuerpo,
                imagen=imagen
            )
            publicacion.save()

            return redirect('previsualizacion', pk=publicacion.pk)
    else:
        form = PublicacionForm()
    return render(request, 'crear_publicacion.html', {'form': form})


@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
    if request.method == "POST":
        publicacion.delete()
        return redirect('mis_publicaciones')
    return render(request, 'eliminar_confirmacion.html', {'publicacion': publicacion})

@login_required
def modificar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk, autor=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect('mis_publicaciones')
    else:
        form = PublicacionForm(instance=publicacion)
    return render(request, 'modificar_publicacion.html', {'form': form, 'publicacion': publicacion})


@login_required
def guardar_publicacion(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == 'POST':
        # Aquí puedes hacer cualquier lógica adicional antes de guardar definitivamente la publicación
        publicacion.save()
        return redirect('mis_publicaciones')
    return render(request, 'previsualizacion.html', {'publicacion': publicacion})