from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from Perfil.models import Usuario

from django.contrib.auth.decorators import login_required #para redirigir a login obligandolo a logearse
from django.contrib.auth import logout

from utils.decorators import check_permiso

# Create your views here.
@login_required
def home(request):
    return render(request, "rol/home.html", {
        'categorias': list(Categoria.objects.all())
    })

@login_required
def listadoCategorias(request):
    return render(request, "rol/listadoCategoria.html", {
        'categorias': list(Categoria.objects.all())
    })


def inicio(request):
    return render(request, "login/inicio.html")


def exit(request):
    logout(request)
    return redirect('inicio')

@login_required
def rol(request):
    return render(request, "rol/gestionRol.html")

#asignar roles
@login_required
@check_permiso('asignar roles', categoria_id=2)
def gestionarRol(request):
    if request.method == 'POST':
        # Obtener los valores seleccionados
        usuario_id = request.POST.get('usuario')
        categoria_id = request.POST.get('categoria')
        rol_id = request.POST.get('rol')
        
        try:
            print(f'categoria id: {categoria_id}')
            print(f'rol id: {rol_id}')
            # Buscar la relación en UsuarioRolCategoria
            usuario_instancia = Usuario.objects.get(user_id=usuario_id)
            print(f'usuario id: {usuario_instancia}')
            usuario_rol_categoria = UsuarioRolCategoria.objects.get(usuario_id=usuario_instancia, categoria_id=categoria_id)

            # Actualizar el rol
            rol_instancia = Rol.objects.get(id=rol_id)
            usuario_rol_categoria.rol = rol_instancia
            usuario_rol_categoria.save()

            # Redirigir a una página de éxito o recargar la página
            return redirect('gestionrol')  # Asegúrate de tener esta URL configurada

        except UsuarioRolCategoria.DoesNotExist:
            usuarios = Usuario.objects.all()
            categorias = Categoria.objects.all()
            roles = Rol.objects.all()
            # Si no existe la relación, puedes manejar el error (opcional)
            print(f'usuario id: {usuario_id}')
            print(f'categoria id: {categoria_id}')
            print(f'rol id: {rol_id}')
            return render(request, 'rol/gestionRol.html', {
                'usuarios': usuarios,
                'categorias': categorias,
                'roles': roles,
            })
    # En caso de GET, renderiza el formulario
    usuarios = Usuario.objects.all()
    categorias = Categoria.objects.all()
    roles = Rol.objects.all()

    return render(request, 'rol/gestionRol.html', {
        'usuarios': usuarios,
        'categorias': categorias,
        'roles': roles,
    })

@login_required
@check_permiso('gestionar roles', categoria_id=2)
def agregarRol(request):
    x = list((Rol.objects.all()).order_by('id'))
    y = list(Permiso.objects.all())
    if request.method == 'GET':
        return render(request, 'rol/crudRol.html', {
            'categorias': list(Categoria.objects.all()),
            'roles': x,
            'permisos': y,
            'form': CreateNewRol()
        })
    else:
        permisos_seleccionados = request.POST.getlist('permisos')
        nuevo_rol = Rol.objects.create(nombre=request.POST['box_nombre'], descripcion=request.POST['box_descripcion'])
        nuevo_rol.permisos.set(permisos_seleccionados)
        nuevo_rol.save()
        return redirect('adicionrol')

@login_required
@check_permiso('gestionar roles', categoria_id=2)
def eliminarRol(request, rol_id):
    #Para que no se eliminen los 5 primeros roles, que son los fundamentales para el funcionamiento de la pagina
    if rol_id > 5: 
        rol_seleccionado = get_object_or_404(Rol, id=rol_id)
        rol_seleccionado.delete()
    return redirect('adicionrol')

@login_required
@check_permiso('gestionar roles', categoria_id=2)
def editarRol(request, rol_id):
    rol = get_object_or_404(Rol, id=rol_id)

    if request.method == 'POST':
        form = CreateNewRol(request.POST)
        if form.is_valid():
            rol.nombre = form.cleaned_data['box_nombre']
            rol.descripcion = form.cleaned_data['box_descripcion']

            permisos_seleccionados = request.POST.getlist('permisos')

            rol.permisos.set(permisos_seleccionados)
            rol.save()
            return redirect('adicionrol')
    else:
        
        form = CreateNewRol(initial={
            'box_nombre': rol.nombre,
            'box_descripcion': rol.descripcion,
            'permisos': list(rol.permisos.all().values_list('id', flat=True))
        })
    

    return render(request, 'rol/editarRol.html', {
        'categorias': list(Categoria.objects.all()),
        'rol': rol,
        'form': form
    })

@login_required
@check_permiso('gestionar categorias', categoria_id=2)
def gestionCategoria(request):
    if request.method == 'GET':
        #Si se entra desde el metodo GET 'visita la pagina'
        x = list((Categoria.objects.all()).order_by('id'))
        return render(request, 'rol/gestionCategoria.html', {
        'categorias': x,
        'form': CreateNewCategoria()
        })
    else:
        #Si se entra desde el metodo POST 'si se envia datos'
        Categoria.objects.create(
            descripcion_corta=request.POST['box_descripcion_corta'], 
            descripcion_larga=request.POST['box_descripcion_larga'], 
            estado=request.POST['box_estado']
        )
        return render(request, 'rol/gestionCategoria.html', {
            'categorias': list(Categoria.objects.all()),
            'form': CreateNewCategoria() 
        })

@login_required
@check_permiso('gestionar categorias', categoria_id=2)
def eliminarCategoria(request, categoria_id):

    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('gestioncategoria')

@login_required
@check_permiso('gestionar categorias', categoria_id=2)
def editarCategoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        form = CreateNewCategoria(request.POST)
        if form.is_valid():
            categoria.descripcion_corta = form.cleaned_data['box_descripcion_corta']
            categoria.descripcion_larga = form.cleaned_data['box_descripcion_larga']
            categoria.estado = form.cleaned_data['box_estado']
            categoria.save()
            return redirect('gestioncategoria')
    else:
        form = CreateNewCategoria(initial={
            'box_descripcion_corta': categoria.descripcion_corta,
            'box_descripcion_larga': categoria.descripcion_larga,
            'box_estado': categoria.estado
        })

    return render(request, 'rol/editarCategoria.html', {
        'categorias': list(Categoria.objects.all()),
        'form': form,
        'categoria': categoria
    })

@login_required
@check_permiso('crear contenido', categoria_id=2)
def seleccionar_plantilla(request):
    return render(request, 'crearpublicaciones/templates/seleccionar_plantilla.html')
   