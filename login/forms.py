from django import forms

class CreateNewCategoria(forms.Form):
    box_descripcion_corta = forms.CharField(label="Descripcion Corta", max_length=100)
    box_descripcion_larga = forms.CharField(label="Descripcion Larga", widget=forms.Textarea)
    # Opciones para el campo Estado
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    box_estado = forms.ChoiceField(label="Estado", choices=ESTADO_CHOICES)