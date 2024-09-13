# utils/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from login.models import UsuarioRolCategoria, Permiso, Usuario

def check_permiso(permiso_nombre, categoria_id):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            try:
                # Lógica para verificar los permisos del usuario en la categoría
                usuario_instancia = Usuario.objects.get(user_id=user)
                usuario_rol = UsuarioRolCategoria.objects.get(usuario=usuario_instancia, categoria_id=categoria_id)
                if usuario_rol.rol.permisos.filter(nombre=permiso_nombre).exists():
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponseForbidden("No tienes permiso para realizar esta acción")
            except UsuarioRolCategoria.DoesNotExist:
                return HttpResponseForbidden("No tienes un rol asignado en esta categoría")
        return _wrapped_view
    return decorator
