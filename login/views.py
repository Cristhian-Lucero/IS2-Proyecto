"""
Vistas de la aplicación login.

Define las vistas para la gestión de categorías, roles, y otras funcionalidades relacionadas
con la autenticación y administración de usuarios.
"""

from django.http import HttpResponse, HttpResponseForbidden
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from Perfil.models import Usuario

from django.contrib.auth.decorators import login_required #para redirigir a login obligandolo a logearse
from django.contrib.auth import logout
from crearpublicaciones.models import Publicacion

from utils.decorators import check_permiso_categoria


# Create your views here.
@login_required
def home(request):
    """
    Renderiza la página principal para usuarios autenticados.

    Argumentos:
        categorias (QuerySet): Lista de todas las categorías disponibles.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/home.html" con el contexto proporcionado.
    """

    return render(request, "rol/home.html", {
        'publicaciones': list((Publicacion.objects.all()).order_by('-fecha_creacion'))
    })

@login_required
def publicacionCategoria(request, descripcion_corta):

    publicaciones = list((Publicacion.objects.all()).order_by('-fecha_creacion'))
    publicacones_filtradas = []
    for i in publicaciones:
        if i.categoria.descripcion_corta == descripcion_corta:
            publicacones_filtradas.append(i)

    return render(request, "rol/publicacionCategoria.html", {
        'publicaciones': publicacones_filtradas,
        'categoria_seleccionada': descripcion_corta
    })


@login_required
def listadoCategorias(request):
    """
    Muestra un listado de todas las categorías.

    Argumentos:
        categorias (QuerySet): Lista de todas las categorías disponibles.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/listadoCategoria.html" con el contexto proporcionado.
    """

    return render(request, "rol/listadoCategoria.html", {
        'categorias': list(Categoria.objects.all())
    })


def inicio(request):
    """
    Renderiza la página de inicio de sesión.

    Retorna:
        HttpResponse: Renderiza la plantilla "login/inicio.html".
    """

    return render(request, "login/inicio.html")


def exit(request):
    """
    Cierra la sesión del usuario y redirige a la página de inicio.

    Retorna:
        HttpResponse: Redirige a la vista "inicio" después de cerrar sesión.
    """

    logout(request)
    return redirect('inicio')

@login_required
def rol(request):
    """
    Renderiza la página de gestión de roles. Requiere que el usuario haya iniciado sesión.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/gestionRol.html".
    """

    return render(request, "rol/gestionRol.html")

#asignar roles
@login_required
@check_permiso_categoria(['gestionar roles'], categoria_id=2)
def gestionarRol(request):
    #retorna True si tiene permiso 'asignar roles' en categoria con id=2
    if confirmarPermiso(request, ['asignar roles'], 2):
        """
        Renderiza la página de gestión de roles con la lista de categorías y roles.
        Maneja solicitudes POST para actualizar el rol de un usuario en una categoría.

        Retorna:
            HttpResponseRedirect: Redirige a 'gestionrol' después de procesar la solicitud.
            HttpResponse: Renderiza la plantilla 'rol/gestionRol.html' en caso de GET o error.
        """

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
    else:
        return HttpResponseForbidden("No tienes un rol asignado en esta categoría")


@login_required
@check_permiso_categoria(['gestionar roles'], categoria_id=2)
def agregarRol(request):
    """
    Permite agregar un nuevo rol al sistema.

    Maneja solicitudes GET para mostrar el formulario y POST para crear el rol.

    Contexto:
        categorias (QuerySet): Lista de todas las categorías.
        roles (QuerySet): Lista de todos los roles existentes.
        permisos (QuerySet): Lista de todos los permisos disponibles.
        form (Form): Instancia del formulario para crear un nuevo rol.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/crudRol.html" o redirige a 'adicionrol' después de crear el rol.
    """

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
@check_permiso_categoria('gestionar roles', categoria_id=2)
def eliminarRol(request, rol_id):
    """
    Elimina un rol específico basado en su ID y redirige a la página de adición de roles.
    Nota:
    No se eliminan los roles con ID menores o iguales a 5, ya que son fundamentales para el funcionamiento de la página.


    Argumentos:
        rol_id (int): El ID del rol a eliminar.

    Retorna:
        HttpResponse: Redirige a 'adicionrol' después de eliminar el rol.
    """

    if rol_id > 5:
        rol_seleccionado = get_object_or_404(Rol, id=rol_id)
        rol_seleccionado.delete()
    rol_seleccionado = get_object_or_404(Rol, id=rol_id)
    rol_seleccionado.delete()
    return redirect('adicionrol')

@login_required
@check_permiso_categoria('gestionar roles', categoria_id=2)
def editarRol(request, rol_id):
    """
    Renderiza la página para editar un rol y maneja la solicitud POST para actualizar los detalles del rol.

    Argumentos:
        rol_id (int): El ID del rol a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/editarRol.html' o actualiza el rol y redirige a 'adicionrol'.
    """

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
@check_permiso_categoria(['gestionar categorias'], categoria_id=2)
def gestionCategoria(request):
    """
    Gestiona la creación y visualización de categorías.

    Maneja solicitudes GET para mostrar el formulario y POST para crear una nueva categoría.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' con la lista de categorías o crea una nueva categoría.
    """

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
@check_permiso_categoria(['gestionar categorias'], categoria_id=2)
def eliminarCategoria(request, categoria_id):
    """
    Elimina una categoría específica identificada por su ID.

    Argumentos:
        categoria_id (int): El ID de la categoría a eliminar.

    Retorna:
        HttpResponse: Redirige a la vista 'gestioncategoria' después de eliminar la categoría.
    """

    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('gestioncategoria')

@login_required
@check_permiso_categoria(['gestionar categorias'], categoria_id=2)
def editarCategoria(request, categoria_id):
    """
    Permite editar una categoría existente.

    Maneja solicitudes GET para mostrar el formulario prellenado y POST para actualizar la categoría.

    Argumentos:
        categoria_id (int): El ID de la categoría a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' o actualiza la categoría y redirige a 'gestioncategoria'.
    """

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

def seleccionar_plantilla(request, categoria_id):
    """
    Vista para seleccionar una plantilla para la publicación.

    Muestra las opciones de plantillas disponibles para ser usadas
    en la creación de publicaciones.

    Returns:
        HttpResponse: Renderiza la página de selección de plantillas.
    """

    return render(request, 'seleccionar_plantilla.html', {
        'categoria_id': categoria_id
    })

def confirmarPermiso(request, permisos, categoria_id):
    user = request.user
    if not user.is_authenticated:
        return False
        
    try:
        # Lógica para verificar los permisos del usuario en la categoría
        usuario_instancia = Usuario.objects.get(user_id=user)
        usuario_rol = UsuarioRolCategoria.objects.get(usuario=usuario_instancia, categoria_id=categoria_id)
        for permiso_nombre in permisos:
            if not usuario_rol.rol.permisos.filter(nombre=permiso_nombre).exists():
                return False
    except UsuarioRolCategoria.DoesNotExist:
        return False
    
    return True
