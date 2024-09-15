# utils/decorators.py
from functools import wraps
from django.http import HttpResponseForbidden
from login.models import UsuarioRolCategoria, Permiso, Usuario
from crearpublicaciones.models import Publicacion
from django.shortcuts import render

def check_permiso_categoria(permisos, categoria_id=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return render(request, 'sin_permiso.html')
                return HttpResponseForbidden("No tienes permiso para realizar esta acción")
            

            local_categoria_id = categoria_id

            print(f"La categoria es ")

            if local_categoria_id is None:
                local_categoria_id = kwargs.get('categoria_id')  # Intentar obtener desde kwargs
                if local_categoria_id is None and len(args) > 1:
                    local_categoria_id = args[1]  # Intentar obtener de los argumentos posicionales

                # Si aún es None, retornar un error
                if local_categoria_id is None:
                    
                    return HttpResponseForbidden("No se proporcionó una categoría válida")

            try:
                # Lógica para verificar los permisos del usuario en la categoría
                usuario_instancia = Usuario.objects.get(user_id=user)
                usuario_rol = UsuarioRolCategoria.objects.get(usuario=usuario_instancia, categoria_id=local_categoria_id)
                
                for permiso_nombre in permisos:
                    if not usuario_rol.rol.permisos.filter(nombre=permiso_nombre).exists():
                        return render(request, 'sin_permiso.html')
                        return HttpResponseForbidden("No tienes permiso para realizar esta acción")
            except UsuarioRolCategoria.DoesNotExist:
                return HttpResponseForbidden("No tienes un rol asignado en esta categoría")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def check_permiso_publicacion_nueva(permisos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return render(request, 'sin_permiso.html')
                return HttpResponseForbidden("No tienes permiso para realizar esta acción")

            local_publicacion_id = kwargs.get('publicacion_id')  # Intentar obtener desde kwargs

            if local_publicacion_id is None and len(args) > 1:
                local_publicacion_id = args[1]  # Intentar obtener de los argumentos posicionales

            # Si aún es None, retornar un error
            if local_publicacion_id is None:
                return HttpResponseForbidden("No se proporcionó una categoría válida")
            
            local_categoria_id = Publicacion.objects.get(id=local_publicacion_id).id

            print(f"La categoria es {local_categoria_id}")

            try:
                # Lógica para verificar los permisos del usuario en la categoría
                usuario_instancia = Usuario.objects.get(user_id=user)
                usuario_rol = UsuarioRolCategoria.objects.get(usuario=usuario_instancia, categoria_id=local_categoria_id)
                
                for permiso_nombre in permisos:
                    if not usuario_rol.rol.permisos.filter(nombre=permiso_nombre).exists():
                        return render(request, 'sin_permiso.html')
                        return HttpResponseForbidden("No tienes permiso para realizar esta acción")
                    print(f"se tiene permiso para '{permiso_nombre}' en la categoria con id {local_categoria_id}")
            except UsuarioRolCategoria.DoesNotExist:
                return HttpResponseForbidden("No tienes un rol asignado en esta categoría")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def check_permiso_publicacion_modificar(permisos):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return render(request, 'sin_permiso.html')
                return HttpResponseForbidden("No tienes permiso para realizar esta acción")
            local_publicacion_id = kwargs.get('publicacion_id')
            if local_publicacion_id is None and len(args) > 1:
                local_publicacion_id = args[1]
            if local_publicacion_id is None:
                return HttpResponseForbidden("No se proporcionó una categoría válida")
            
            #Aca comienza la logica
            try:
                # Lógica para verificar los permisos del usuario en la categoría
                publicacion_acceso = Publicacion.objects.get(id=local_publicacion_id)
                local_categoria_id = publicacion_acceso.id
                usuario_instancia = Usuario.objects.get(user_id=user)
                usuario_rol = UsuarioRolCategoria.objects.get(usuario=usuario_instancia, categoria_id=local_categoria_id)

                
                if user.id != publicacion_acceso.user.id and not usuario_rol.rol.permisos.filter(nombre='gestionar contenido otros').exists():
                    return HttpResponseForbidden("No vayas a tocar cosa ajena. Ish")
                
                for permiso_nombre in permisos:
                    if not usuario_rol.rol.permisos.filter(nombre=permiso_nombre).exists():
                        return render(request, 'sin_permiso.html')
                        return HttpResponseForbidden("No tienes permiso para realizar esta acción")
                        
            except UsuarioRolCategoria.DoesNotExist:
                return HttpResponseForbidden("No tienes un rol asignado en esta categoría")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator