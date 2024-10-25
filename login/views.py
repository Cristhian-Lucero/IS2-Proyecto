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
    """
    Vista para la gestión de los ajustes de usuario, permitiendo actualizar nombre y apellido, foto de perfil, biografía, email y contraseña.

    Muestra diferentes formularios dependiendo del tipo de ajuste seleccionado.

    Argumentos:
        request (HttpRequest): La solicitud HTTP que contiene la información del formulario enviado (si corresponde).

    Formularios manejados:
        - `foto_bio`: Actualización de foto de perfil y biografía.
        - `nombre_apellido`: Actualización de nombre y apellido.
        - `email`: Actualización de email.
        - `contrasena`: Actualización de la contraseña.

    Retorna:
        HttpResponse: Renderiza la plantilla 'login/ajustes.html' con los formularios correspondientes y sus instancias.
    """

    perfil = request.user
    instancia = Usuario.objects.get(user_id=perfil.id)  # Obtenemos la instancia de Usuario

    if request.method == 'POST':
        form_nombre_apellido = UpdateNombreApellido(request.POST, request=request)
        form_foto_bio = PerfilForm(request.POST, request.FILES, instance=instancia, request=request)
        form_nuevo_email = UpdateEmail(request.POST, request=request)
        form_nueva_contrasena = UpdatePassword(request.POST, request=request)

        if request.POST.get('form_type') == 'foto_bio':

            if form_foto_bio.is_valid():
                form_foto_bio.save()
                return redirect(reverse('perfil', kwargs={'username': request.user.username}))  # Redirige al perfil después de guardar

        elif request.POST.get('form_type') == 'nombre_apellido':

            if form_nombre_apellido.is_valid():
                form_nombre_apellido.save()  # Llamamos al método save para actualizar el usuario
                return redirect(reverse('perfil', kwargs={'username': request.user.username}))  # Redirigimos al perfil
        
        elif request.POST.get('form_type') == 'email':

                if form_nuevo_email.is_valid():
                    form_nuevo_email.save()  # Llamamos al método save para actualizar el usuario
                    return redirect(reverse('perfil', kwargs={'username': request.user.username}))  # Redirigimos al perfil
        
        elif request.POST.get('form_type') == 'contrasena':

                if form_nueva_contrasena.is_valid():
                    form_nueva_contrasena.save()  # Llamamos al método save para actualizar el usuario
                    return redirect(reverse('perfil', kwargs={'username': request.user.username}))  # Redirigimos al perfil
    
    else:
        form_foto_bio = PerfilForm(instance=instancia, request=request)
        form_nombre_apellido = UpdateNombreApellido(request=request)
        form_nuevo_email = UpdateEmail(request=request)
        form_nueva_contrasena = UpdatePassword(request=request)

    return render(request, 'login/ajustes.html', {
        'form_foto_bio': form_foto_bio,
        'form_nombre_apellido': form_nombre_apellido,
        'form_nuevo_email': form_nuevo_email,
        'form_nueva_contrasena': form_nueva_contrasena
    })


@login_required
def perfil(request, username):
    """
    Vista para mostrar el perfil de un usuario específico basado en su nombre de usuario.

    Muestra las publicaciones del usuario, así como información adicional como el total de likes y vistas.

    Argumentos:
        request (HttpRequest): La solicitud HTTP.
        username (str): El nombre de usuario del perfil que se desea mostrar.

    Retorna:
        HttpResponse: Renderiza la plantilla 'login/perfil.html' con la información del usuario y sus publicaciones.
    """

    usuario = User.objects.get(username=username)
    publicacion_usuario = Publicacion.objects.filter(user=usuario)
    usuario_datos_extra = Usuario.objects.get(user_id=usuario.id)

    likes = 0
    vistas = 0
    publicacion_usuario_filtrado = []
    for i in list(publicacion_usuario.order_by('-fecha_creacion')):
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

@login_required
def eliminar_usuario(request, user_id):
    """
    Vista para eliminar un usuario específico basado en su ID.

    Argumentos:
        request (HttpRequest): La solicitud HTTP.
        user_id (int): El ID del usuario que se desea eliminar.

    Retorna:
        HttpResponse: Redirige a la página principal 'home' después de eliminar el usuario.
    """
    
    usuario = User.objects.get(id=user_id)
    usuario.delete()
    return redirect('home')