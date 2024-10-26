from django import template
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def solo_parrafos(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    paragraphs = soup.find_all('p')
    return ' '.join([p.get_text() for p in paragraphs])

@register.filter
def resta_fechas(fecha_publicacion, fecha_creacion):
    delta = fecha_publicacion - fecha_creacion

    dias = delta.days
    segundos_totales = delta.seconds
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60

    # Formatear la cadena de salida
    resultado = f"{dias} días {horas} horas {minutos} minutos y {segundos} segundos"
    return resultado

@register.filter
def formatear_timedelta(delta):
    # Extraer días, segundos, horas, y minutos del timedelta
    dias = delta.days
    segundos_totales = delta.seconds
    horas = segundos_totales // 3600
    minutos = (segundos_totales % 3600) // 60
    segundos = segundos_totales % 60

    # Formatear la cadena de salida
    resultado = f"{dias} días {horas} horas {minutos} minutos y {segundos} segundos"
    return resultado

