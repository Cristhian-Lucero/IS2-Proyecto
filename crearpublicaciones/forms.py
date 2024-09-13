"""
Formularios para el modelo 'crearpublicaciones'.
"""

from django import forms
from .models import Publicacion

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
        fields = ['titulo', 'texto_corto', 'texto_largo', 'cita', 'imagen1', 'imagen2']

    def clean(self):
        cleaned_data = super().clean()

        # Verificar que solo se suban hasta dos imágenes
        imagen1 = cleaned_data.get("imagen1")
        imagen2 = cleaned_data.get("imagen2")

        if not imagen1 and not imagen2:
            raise forms.ValidationError("Debes subir al menos una imagen.")

        texto_corto = cleaned_data.get("texto_corto")
        if len(texto_corto) > 150:
            self.add_error('texto_corto', 'El texto corto no puede tener más de 150 caracteres.')
