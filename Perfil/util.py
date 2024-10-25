
from django.core.mail import send_mail
from django.conf import settings

def enviar_notificacion_cambio_estado(usuario, publicacion):
    asunto = 'Tu publicación ha cambiado de estado'
    mensaje = f'Hola {usuario.username}, tu publicación "{publicacion.titulo}" ha cambiado de estado.'
    destinatario = [usuario.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)

def enviar_notificacion_modificacion(autor, publicacion):
    asunto = 'Tu publicación ha sido modificada'
    mensaje = f'Hola {autor.username}, tu publicación "{publicacion.titulo}" ha sido modificada.'
    destinatario = [autor.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)

def enviar_notificacion_comentario(autor, publicacion, comentario):
    asunto = 'Nuevo comentario en tu publicación'
    mensaje = f'Hola {autor.username}, hay un nuevo comentario en tu publicación "{publicacion.titulo}": "{comentario.texto}".'
    destinatario = [autor.email]
    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, destinatario)
