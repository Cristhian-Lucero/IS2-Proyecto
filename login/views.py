"""
Vistas de la aplicación login.

Define las vistas para la gestión de categorías, roles, y otras funcionalidades relacionadas
con la autenticación y administración de usuarios.
"""

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from crearpublicaciones.models import Comentario
from django.contrib.auth.decorators import login_required 
from crearpublicaciones.models import Publicacion
from Perfil.models import *
from Perfil.forms import *

from django.core.paginator import Paginator
from django.urls import reverse
from django.contrib.auth import logout

from utils.decorators import check_permiso_categoria
from .utils import *
from django.contrib.auth.models import User

from django.db.models import Q

@login_required
def home(request):
    """
    Renderiza la página principal para usuarios autenticados.

    Argumentos:
        categorias (QuerySet): Lista de todas las categorías disponibles.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/home.html" con el contexto proporcionado.
    """
    publicaciones = list((Publicacion.objects.all()).order_by('-fecha_creacion'))
    publicacones_filtradas = []
    numero_comentarios = []
    for i in publicaciones:
        if i.estado == 'publicado':
            publicacones_filtradas.append(i)

    paginator = Paginator(publicacones_filtradas, 10)  # Muestra 10 publicaciones por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "rol/home.html", {
        'page_obj': page_obj
    })

@login_required
def publicacionCategoria(request, descripcion_corta):

    publicaciones = list((Publicacion.objects.all()).order_by('-fecha_creacion'))
    publicacones_filtradas = []
    for i in publicaciones:
        if i.categoria.descripcion_corta == descripcion_corta:
            if i.estado == 'publicado':
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

#eliminar(?
@login_required
def rol(request):
    """
    Renderiza la página de gestión de roles. Requiere que el usuario haya iniciado sesión.

    Retorna:
        HttpResponse: Renderiza la plantilla "rol/gestionRol.html".
    """
    return render(request, "rol/gestionRol.html")

@login_required
def gestionarRol(request):
    """
    Renderiza la página de gestión de roles con la lista de categorías y roles.
    Maneja solicitudes POST para actualizar el rol de un usuario en una categoría.

    Retorna:
        HttpResponseRedirect: Redirige a 'gestionrol' después de procesar la solicitud.
        HttpResponse: Renderiza la plantilla 'rol/gestionRol.html' en caso de GET o error.
    """

    if not verificar_permisos_admin(request, ['gestionar roles']):
        return render(request, 'sin_permiso.html')
    
    if request.method == 'POST':
        # Obtener los valores seleccionados
        usuario_id = request.POST.get('usuario')
        print(f'el user id del form es {usuario_id}')
        categoria_id = request.POST.get('categoria')
        rol_id = request.POST.get('rol')

        try:
            # Buscar la relación en UsuarioRolCategoria
            usuario_instancia = Usuario.objects.get(user_id=usuario_id)
            print(f'el user id del filtrado es {usuario_instancia}')
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
            return render(request, 'rol/gestionRol.html', {
                'usuarios': usuarios,
                'categorias': categorias,
                'roles': roles,
            })
    # En caso de GET, renderiza el formulario
    usuarios = Usuario.objects.all().order_by('user__username')
    categorias = Categoria.objects.all()
    roles = Rol.objects.all()
    gestion = list(UsuarioRolCategoria.objects.all().order_by('usuario'))

    return render(request, 'rol/gestionRol.html', {
        'usuarios': usuarios,
        'categorias': categorias,
        'roles': roles,
        'usuarioRolCategoria': gestion
    })

@login_required
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

    if not verificar_permisos_admin(request, ['gestionar roles']):
        return render(request, 'sin_permiso.html')

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
    if not verificar_permisos_admin(request, ['gestionar roles']):
        return render(request, 'sin_permiso.html')

    if rol_id > 5:
        rol_seleccionado = get_object_or_404(Rol, id=rol_id)
        rol_seleccionado.delete()
    rol_seleccionado = get_object_or_404(Rol, id=rol_id)
    rol_seleccionado.delete()
    return redirect('adicionrol')

@login_required
def editarRol(request, rol_id):
    """
    Renderiza la página para editar un rol y maneja la solicitud POST para actualizar los detalles del rol.

    Argumentos:
        rol_id (int): El ID del rol a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/editarRol.html' o actualiza el rol y redirige a 'adicionrol'.
    """
    if not verificar_permisos_admin(request, ['gestionar roles']):
        return render(request, 'sin_permiso.html')

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
def gestionCategoria(request):
    """
    Gestiona la creación y visualización de categorías.

    Maneja solicitudes GET para mostrar el formulario y POST para crear una nueva categoría.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' con la lista de categorías o crea una nueva categoría.
    """
    if not verificar_permisos_admin(request, ['gestionar categorias']):
        return render(request, 'sin_permiso.html')

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
def eliminarCategoria(request, categoria_id):
    """
    Elimina una categoría específica identificada por su ID.

    Argumentos:
        categoria_id (int): El ID de la categoría a eliminar.

    Retorna:
        HttpResponse: Redirige a la vista 'gestioncategoria' después de eliminar la categoría.
    """

    if not verificar_permisos_admin(request, ['gestionar categorias']):
        return render(request, 'sin_permiso.html')

    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.delete()
    return redirect('gestioncategoria')

@login_required
def editarCategoria(request, categoria_id):
    """
    Permite editar una categoría existente.

    Maneja solicitudes GET para mostrar el formulario prellenado y POST para actualizar la categoría.

    Argumentos:
        categoria_id (int): El ID de la categoría a editar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'rol/gestionCategoria.html' o actualiza la categoría y redirige a 'gestioncategoria'.
    """

    if not verificar_permisos_admin(request, ['gestionar categorias']):
        return render(request, 'sin_permiso.html')

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
@check_permiso_categoria(['crear contenido'])
def seleccionar_plantilla(request, categoria_id):
    """
    Vista para seleccionar una plantilla para la publicación.

    Muestra las opciones de plantillas disponibles para ser usadas
    en la creación de publicaciones.

    Returns:
        HttpResponse: Renderiza la página de selección de plantillas.
    """

    if not verificar_permisos_categoria_id(request, ['crear contenido'], categoria_id):
        return render(request, 'sin_permiso.html')

    return render(request, 'seleccionar_plantilla.html', {
        'categoria_id': categoria_id
    })

@login_required
def ajustes(request):
    perfil = request.user
    if request.method == 'POST':
        # Pasamos los archivos subidos (FILES) y los datos del formulario (POST)
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        
        if form.is_valid():
            form.save() 
            return redirect(reverse('perfil', kwargs={'username': request.user.username}))  # Redirige al perfil después de guardar

    else:
        
        form = PerfilForm(instance=perfil)

    return render(request, 'login/ajustes.html', {'form': form})


@login_required
def perfil(request, username):
    usuario = User.objects.get(username=username)
    publicacion_usuario = Publicacion.objects.filter(user=usuario)
    usuario_datos_extra = Usuario.objects.get(user_id=usuario.id)

    likes = 0
    vistas = 0
    publicacion_usuario_filtrado = []
    for i in publicacion_usuario:
        if i.estado == "publicado":
            likes += i.me_gustas
            vistas += i.vistas
            publicacion_usuario_filtrado.append(i)

    return render(request, 'login/perfil.html', {
        'usuario': usuario,
        'publicaciones': publicacion_usuario_filtrado,
        'usuario_extra': usuario_datos_extra,
        'likes': likes,
        'vistas': vistas
    })

def search(request):

    return render(request, 'search/busqueda_contenido.html', {
        'publicaciones': list((Publicacion.objects.all()).order_by('-fecha_creacion'))
    })

def filtrar_publicaciones(request):
    """
    Filtra las publicaciones según los parámetros proporcionados en la solicitud GET.

    Parameters:
        request (HttpRequest): Objeto de solicitud que contiene los parámetros de búsqueda.
            - keyword (str): Palabra clave para buscar en el título o contenido de las publicaciones.
            - category (str): Categoría de la publicación.
            - status (str): Estado de la publicación.
            - date-from (str): Fecha desde la cual filtrar las publicaciones.
            - autor (str): Nombre de usuario del autor de la publicación.

    Returns:
        HttpResponse: Renderiza la pagina con el contexto de las publicaciones filtradas.
    """
    # Obtener los valores del filtro desde la URL (GET)
    keyword = request.GET.get('keyword', '')
    categoria = request.GET.get('category', '')
    fecha = request.GET.get('date-from', '')
    autor = request.GET.get('autor', '')

    # Filtrar las publicaciones
    publicaciones = Publicacion.objects.all().order_by('-fecha_creacion')

    if keyword:
        publicaciones = publicaciones.filter(Q(titulo__icontains=keyword) | Q(contenido_html__icontains=keyword))
    if categoria:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__iexact=categoria)
    if fecha:
        publicaciones = publicaciones.filter(fecha_creacion__gte=fecha)
    if autor:
        publicaciones = publicaciones.filter(user__username__icontains=autor)

    # Paginación de las publicaciones filtradas
    paginator = Paginator(publicaciones, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'rol/home.html', {
        'page_obj': page_obj,
        'keyword': keyword,
        'categoria': categoria,
        'fecha': fecha,
        'autor': autor})