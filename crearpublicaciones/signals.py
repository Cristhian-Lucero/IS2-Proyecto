
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse
from .models import Publicacion, Comentario

@receiver(pre_save, sender=Publicacion)
def notificar_cambios_publicacion(sender, instance, **kwargs):
    if instance.id is not None:
        publicacion_anterior = Publicacion.objects.get(id=instance.id)
        usuario = instance.user

        # Verificar si el estado ha cambiado
        if publicacion_anterior.estado != instance.estado:
            asunto = 'Tu publicación ha cambiado de estado'
            mensaje_html = render_to_string('emails/publicacion_cambio_estado.html', {
                'usuario': usuario,
                'publicacion': instance,
            })
            mensaje = EmailMultiAlternatives(asunto, '', settings.EMAIL_HOST_USER, [usuario.email])
            mensaje.attach_alternative(mensaje_html, "text/html")
            mensaje.send()

        # Verificar si el título o contenido han cambiado
        elif publicacion_anterior.titulo != instance.titulo or publicacion_anterior.contenido_html != instance.contenido_html:
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
