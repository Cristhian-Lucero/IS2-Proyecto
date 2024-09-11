from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio/', inicio, name='inicio'),
    path('logout/',exit,name='exit'),
    path('rol/', rol, name='rol' ),

    path('home/', home, name='home'),
    path('home/lista_categoria', listadoCategorias, name='lista_categoria'),

    path('gestionrol/', gestionarRol, name='gestionrol'),
    
    path('adicionrol/', agregarRol, name='adicionrol'),
    path('editar_rol/<int:rol_id>/', editarRol, name='editar_rol'),
    path('eliminar_rol/<int:rol_id>/', eliminarRol, name='eliminar_rol'),

    path('gestioncategoria/', gestionCategoria, name='gestioncategoria'),
    path('editar_categoria/<int:categoria_id>/', editarCategoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', eliminarCategoria, name='eliminar_categoria'),

    path('seleccionar-plantilla/', seleccionar_plantilla, name='seleccionar_plantilla'),
]


#Todavia no está terminado
def usuario_tiene_permiso(usuario, permiso_nombre):
    try:
        usuario_instancia = Usuario.objects.get(user_id=usuario)
        usuario_rol = UsuarioRolCategoria.objects.get(usuario_id=usuario_instancia)
        rol = usuario_rol.rol_id
        return Rol.objects.get(nombre=permiso_nombre).exists()
    except UsuarioRolCategoria.DoesNotExist:
        return False
