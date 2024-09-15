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

def permisos_categoria_usuario_context(request):
    if not request.user.is_authenticated:
        return {}

    user = Usuario.objects.get(user_id=request.user)
    usuario_instancia = user
    roles_usuario = UsuarioRolCategoria.objects.filter(usuario=usuario_instancia)
    permisos = {}

    ######################################################
    # roles_usuarios =

    #  USUARIO       ROL           CATEGORIA
    # ivan_renee - Suscriptor - Inteligencia Artificial
	# ivan_renee - Suscriptor - Ciencia de datos
	# ivan_renee - Publicador - Energías Renovables
	# ivan_renee - Suscriptor - TIC
	# ivan_renee - Suscriptor - Robótica
	# ivan_renee - Suscriptor - Ciberseguridad
    ######################################################

    for i in roles_usuario:
        if i.categoria.id not in permisos:
            permisos[i.categoria.id] = []

        for j in i.rol.permisos.all():
            permisos[i.categoria.id].append(j.nombre)

     ######################################################
    #   Permisos =
    #
    # Inteligencia Artificial : ['permiso1', 'permiso2', ..., 'permisoN']
	# Ciencia de datos : ['permiso1', 'permiso2', ..., 'permisoN']
	# Energías Renovables : ['permiso1', 'permiso2', ..., 'permisoN']
	# TIC : ['permiso1', 'permiso2', ..., 'permisoN']
	# Robótica : ['permiso1', 'permiso2', ..., 'permisoN']
	# Ciberseguridad : ['permiso1', 'permiso2', ..., 'permisoN']
    ######################################################

    return {
        'permisos_categoria': permisos,
        'user': user.user
        }


