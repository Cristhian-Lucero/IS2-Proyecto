'''
Signals para notificaciones de cambios en publicaciones y nuevos comentarios.
'''
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from .models import Publicacion, Comentario

@receiver(post_save, sender=Publicacion)
def notificar_cambios_publicacion(sender, instance, created, **kwargs):
    """
    Envía una notificación por correo electrónico al usuario cuando se detectan cambios en una publicación.

    Esta función se ejecuta después de guardar una instancia de 'Publicacion'.
    Utiliza el parámetro 'created' para determinar si la instancia es nueva o existente.
    """

    usuario = instance.user

    if created:
        # La publicación es nueva. No enviar notificación de modificación.
        pass
    else:
        # La publicación ha sido modificada
        asunto = 'Tu publicación ha sido modificada'
        mensaje_html = render_to_string('emails/publicacion_modificada.html', {
            'usuario': usuario,
            'publicacion': instance,
        })
        mensaje = EmailMultiAlternatives(asunto, '', settings.EMAIL_HOST_USER, [usuario.email])
        mensaje.attach_alternative(mensaje_html, "text/html")
        mensaje.send()



@receiver(post_save, sender=Comentario)
def notificar_nuevo_comentario(sender, instance, created, **kwargs):
    """
    Envía una notificación por correo electrónico al autor de una publicación cuando un nuevo comentario es agregado.

    Esta función se ejecuta después de guardar una instancia de 'Comentario'.
    Verifica si el comentario fue creado por un usuario distinto al autor de la publicación
    y, de ser así, envía un correo electrónico al autor de la publicación.

    Args:
        sender (class): El modelo que envía la señal (en este caso, 'Comentario').
        instance (Comentario): La instancia del comentario que se ha guardado.
        created (bool): Indica si la instancia del comentario fue creada o solo modificada.
        **kwargs: Argumentos adicionales proporcionados por la señal.
    """
    
    if created:
        publicacion = instance.publicacion
        autor_publicacion = publicacion.user
        autor_comentario = instance.user

        if autor_publicacion != autor_comentario:
            asunto = 'Nuevo comentario en tu publicación'
            mensaje_html = render_to_string('emails/nuevo_comentario.html', {
                'autor_publicacion': autor_publicacion,
                'autor_comentario': autor_comentario,
                'publicacion': publicacion,
                'comentario': instance,
            })
            mensaje = EmailMultiAlternatives(asunto, '', settings.EMAIL_HOST_USER, [autor_publicacion.email])
            mensaje.attach_alternative(mensaje_html, "text/html")
            mensaje.send()
