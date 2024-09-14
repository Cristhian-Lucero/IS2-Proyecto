from login.models import Categoria, UsuarioRolCategoria
from Perfil.models import Usuario

def categorias_context(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}

def permisos_usuario_context(request):
    if not request.user.is_authenticated:
        return {}

    # Obtener todos los roles y permisos del usuario
    usuario_instancia = Usuario.objects.get(user_id=request.user)
    roles_usuario = UsuarioRolCategoria.objects.filter(usuario=usuario_instancia)
    permisos = set()  # Usamos un set para evitar duplicados
    
    for rol_categoria in roles_usuario:
        for permiso in rol_categoria.rol.permisos.all():
            permisos.add(permiso.nombre)

    # Devolvemos los permisos en el contexto para que sean accesibles en los templates
    return {'permisos_usuario': permisos}
