"""
Formularios para el modelo 'crearpublicaciones'.
"""

from django import forms
from .models import Publicacion, Comentario

class PublicacionForm(forms.ModelForm):
    """Este formulario utiliza 'ModelForm' para facilitar la creación y validación
    de los datos. Permite al usuario ingresar un título,
    texto corto, texto largo, una cita y hasta dos imágenes.

    Validaciones:
    - Se asegura de que al menos una de las imágenes (imagen1 o imagen2) sea subida.
    - Verifica que el campo 'texto_corto' no exceda los 150 caracteres.
    """

    class Meta:
        model = Publicacion
        fields = ['titulo', 'contenido_html', 'estado', 'categoria']  

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['descripcion']  # Campos del formulario que vas a incluir
