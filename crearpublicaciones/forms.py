from django import forms
from .models import Publicacion

class PublicacionForm(forms.ModelForm):
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
