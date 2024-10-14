"""
Vistas de la aplicación Perfil.

Define las vistas para la gestión de Perfiles.
"""


from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Usuario

# Vista basada en clases para mostrar el perfil del usuario autenticado
class PerfilDetailView(LoginRequiredMixin, DetailView):
    """
    Vista basada en clases para mostrar el perfil del usuario autenticado.

    Attributes:
        model (Model): Modelo que representa el perfil de usuario (Usuario).
        template_name (str): Plantilla que se usará para renderizar la vista.
        context_object_name (str): Nombre con el que se accederá al objeto en la plantilla.
    """

    model = Usuario  # Modelo que representa el perfil de usuario
    template_name = 'perfil/ver_perfil.html'  # Plantilla que se usará para la vista
    context_object_name = 'usuario'  # Nombre con el que se accederá al objeto en la plantilla

    def get_object(self):
        """
        Retorna el perfil del usuario autenticado. 
        Usamos el método get_object para obtener el perfil del usuario actual.
        """
        return get_object_or_404(Usuario, user=self.request.user)

# Create your views here.

from django.shortcuts import render, redirect
from .forms import PerfilForm

def perfil_update(request):
    # Obtener el usuario actual
    if request.method == 'POST':
        usuario_actual = request.user
        instancia = Usuario.objects.get(user_id=usuario_actual)
        form = PerfilForm(request.POST, request.FILES, instance=instancia)  # instance vincula con el usuario actual
        if form.is_valid():
            form.save()  # Guarda los datos en la base de datos
            return redirect('perfil')  # Redirige a alguna página (ajusta según tu ruta)
    else:
        form = PerfilForm(instance=request.user.usuario)  # Cargar el formulario con datos existentes del usuario

    return render(request, 'perfil.html', {'form': form})

