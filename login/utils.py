from .models import *
from crearpublicaciones.models import *
from Tablero.models import *

def verificar_permisos_admin(request, permisos_requeridos):
    usuario_instancia = Usuario.objects.get(user_id=request.user)
    rol_categoria = UsuarioRolCategoria.objects.filter(usuario=usuario_instancia)

    flag = False

    # Iterar sobre los roles del usuario
    for rol_cat in rol_categoria:
        permisos_rol = rol_cat.rol.permisos.all()

        for permiso_requerido in permisos_requeridos:
            if permiso_requerido in [permiso.nombre for permiso in permisos_rol]:
                flag = True
                break

        if flag:
            break

    return flag

def verificar_permisos_categoria_id(request, permisos_requeridos, categoria_id):

    usuario_instancia = Usuario.objects.get(user_id=request.user)
    rol = UsuarioRolCategoria.objects.filter(usuario=usuario_instancia, categoria_id=categoria_id)
    flag = False

    for rol_cat in rol:
        permisos_rol = rol_cat.rol.permisos.all()

        for permiso_requerido in permisos_requeridos:
            if permiso_requerido in [permiso.nombre for permiso in permisos_rol]:
                flag = True
                break

        if flag:
            break

    return flag