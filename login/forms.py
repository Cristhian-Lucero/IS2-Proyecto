from django import forms
from .models import *

class CreateNewCategoria(forms.Form):
    box_descripcion_corta = forms.CharField(label="Descripcion Corta", max_length=100)
    box_descripcion_larga = forms.CharField(label="Descripcion Larga", widget=forms.Textarea)
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    box_estado = forms.ChoiceField(label="Estado", choices=ESTADO_CHOICES)

class CreateNewRol(forms.Form):
    box_nombre= forms.CharField(label="Nombre", max_length=100)
    box_descripcion = forms.CharField(
        label="Descripcion", 
        widget=forms.Textarea (attrs={'rows': 5, 'cols': 50, 'style': 'width:100%;'}))

    def __init__(self, *args, **kwargs):
        super(CreateNewRol, self).__init__(*args, **kwargs)
        permisos_choices = [(permiso.id, permiso.nombre) for permiso in Permiso.objects.all()]
        self.fields['permisos'] = forms.MultipleChoiceField(
            label="Permisos",
            choices=permisos_choices,
            widget=forms.CheckboxSelectMultiple
        )

