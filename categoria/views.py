from django.shortcuts import render

# Create your views here.
def listar_categorias(request):
    return render(request, 'listar_categorias.html')
