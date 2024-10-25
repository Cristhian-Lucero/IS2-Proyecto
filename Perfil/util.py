"""
Este módulo proporciona funciones para enviar notificaciones automáticas por correo en eventos relacionados con las publicaciones del usuario.
"""

from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_cambio_estado(usuario, publicacion):
    """
    Envía una notificación por correo al usuario cuando su publicación ha cambiado de estado.

    Args:
        usuario (User): Objeto de usuario que recibe la notificación. Debe tener un atributo 'username' y 'email'.
        publicacion (Publicacion): Objeto de la publicación que ha cambiado de estado. Debe tener un atributo 'titulo'.
    """

    asunto = 'Tu publicación ha cambiado de estado'
    mensaje = f'Hola {usuario.username}, tu publicación "{publicacion.titulo}" ha cambiado de estado.'
    destinatario = [usuario.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)

def enviar_notificacion_modificacion(autor, publicacion):
    """
    Envía una notificación por correo al autor cuando su publicación ha sido modificada.

    Args:
        autor (User): Objeto de usuario que es el autor de la publicación. Debe tener un atributo 'username' y 'email'.
        publicacion (Publicacion): Objeto de la publicación que ha sido modificada. Debe tener un atributo 'titulo'.
    """

    asunto = 'Tu publicación ha sido modificada'
    mensaje = f'Hola {autor.username}, tu publicación "{publicacion.titulo}" ha sido modificada.'
    destinatario = [autor.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)

def enviar_notificacion_comentario(autor, publicacion, comentario):
    """
    Envía una notificación por correo al autor de una publicación cuando hay un nuevo comentario.

    Args:
        autor (User): Objeto de usuario que es el autor de la publicación. Debe tener un atributo 'username' y 'email'.
        publicacion (Publicacion): Objeto de la publicación que ha recibido un comentario. Debe tener un atributo `titulo`.
        comentario (Comentario): Objeto del comentario. Debe tener un atributo `texto`.
    """

    asunto = 'Nuevo comentario en tu publicación'
    mensaje = f'Hola {autor.username}, hay un nuevo comentario en tu publicación "{publicacion.titulo}": "{comentario.texto}".'
    destinatario = [autor.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)
