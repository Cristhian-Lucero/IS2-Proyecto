import time
from datetime import timedelta, datetime
from django.utils import timezone
import pytz

def verificar_inactividad_task():
    from .models import Publicacion, Historial
    primera_ejecucion = True
    while True:
        if not primera_ejecucion:
            # Obtiene la fecha actual
            fecha_actual = timezone.now().astimezone(pytz.timezone('America/Asuncion'))

            # Obtiene la fecha límite (hace 30 días)
            fecha_limite = fecha_actual - timedelta(days=30)

            # Obtiene las publicaciones que caducaron
            publicaciones = Publicacion.objects.filter(fecha_publicacion__lte=fecha_limite, estado='publicado')

            # Verifica si se encontraron publicaciones inactivas
            if publicaciones.exists():

                # Actualiza el estado de las publicaciones a inactivo
                publicaciones.update(estado='inactivo')

                # Crear un registro en el historial de cambios
                for publicacion in publicaciones:
                    Historial.objects.create(
                        publicacion=publicacion,
                        usuario="Sistema",
                        accion='inactivado'
                    )

            # Calcula los segundos que faltan hasta medianoche
            segundos_hasta_medianoche = 86400 - ((fecha_actual.hour * 60 + fecha_actual.minute) * 60 + fecha_actual.second)

            # Espera hasta medianoche para volver a verificar
            time.sleep(segundos_hasta_medianoche)
        else:
            primera_ejecucion = False
            time.sleep(1)
