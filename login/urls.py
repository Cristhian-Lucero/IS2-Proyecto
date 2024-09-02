from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio/', inicio, name='inicio'),
    path('base/', base, name='base'),
    path('base2/', base2, name='base2'),
    path('logout/',exit,name='exit'),
    path('rol/', rol, name='rol' ),

    path('gestionrol/', gestionarRol),
    
    path('adicionrol/', agregarRol, name='adicionrol'),
    path('eliminar_rol/<int:rol_id>/', eliminarRol, name='eliminar_rol'),

    path('gestioncategoria/', gestionCategoria, name='gestioncategoria'),
    path('editar_categoria/<int:categoria_id>/', editarCategoria, name='editar_categoria'),
    path('eliminar_categoria/<int:categoria_id>/', eliminarCategoria, name='eliminar_categoria'),
    
    # Permiso URLs
    path('api/permisos/', PermisoListCreate.as_view(), name='permiso-list-create'),
    path('api/permisos/<int:pk>/', PermisoRetrieveUpdateDestroy.as_view(), name='permiso-detail'),

    # Rol URLs
    path('api/roles/', RolListCreate.as_view(), name='rol-list-create'),
    path('api/roles/<int:pk>/', RolRetrieveUpdateDestroy.as_view(), name='rol-detail'),

    # Categoria URLs
    path('api/categorias/', CategoriaListCreate.as_view(), name='categoria-list-create'),
    path('api/categorias/<int:pk>/', CategoriaRetrieveUpdateDestroy.as_view(), name='categoria-detail'),

    # Usuario URLs
    path('api/usuarios/', UsuarioListCreate.as_view(), name='usuario-list-create'),
    path('api/usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroy.as_view(), name='usuario-detail'),
]
