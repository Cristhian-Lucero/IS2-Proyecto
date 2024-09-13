from login.models import Categoria  # Asegúrate de importar el modelo correctamente

def categorias_context(request):
    categorias = Categoria.objects.all()
    return {'categorias': categorias}