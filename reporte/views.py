from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import *
from login.models import *
from .models import *

# Create your views here.

@login_required
def masVistos(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas

    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.all()
    publicaciones = publicaciones.order_by('-vistas')


    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'masVistos.html', {
            'publicaciones': list(publicaciones.order_by('-vistas')), 
            'categorias': Categoria.objects.all()
            })
    
    else:
        html_content = """
            <div class="articles">
                <h2 style="text-align: center;">Top más vistos</h2>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones[:10]:
            texto = f"""
            <div class="article">
                <h2 style="text-transform: uppercase;">{ i.titulo }</h2>
                <h3>Vistas: { i.vistas }</h3>
                <a href="/home/categoria/{i.categoria.descripcion_corta}">{ i.categoria.descripcion_corta } <br></a> 
                <p>Autor: <a href="/perfil/{i.user}">{i.user}</a></p>
                <p>Fecha: { i.fecha_creacion } </p>
                <button class="toggle-button" onclick="toggleContent('contenido-{i.id}')">Mostrar contenido</button>
                <a class="read-more" href="/crearpublicaciones/previsualizar/{ i.id }">IR A PAGINA</a>
                <div id="contenido-{i.id}" class="contenido"> {i.contenido_html} </div>
            </div>
            """
            html_content += texto  # Esta línea debería estar alineada correctamente dentro del bucle.

        html_content += "</div>"  # Añadido fuera del bucle.


        nuevo_reporte = Reporte.objects.create()

        nuevo_reporte.titulo = titulo
        nuevo_reporte.html_content = html_content
        nuevo_reporte.user = request.user.username
        nuevo_reporte.tipo = 'mas leido'

        nuevo_reporte.save()
        return redirect('listaReportes')

@login_required
def masLikeados(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas
    
    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.all()
    publicaciones = publicaciones.order_by('-me_gustas')

    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'masLikeados.html', {
            'publicaciones': list(publicaciones.order_by('-me_gustas')), 
            'categorias': Categoria.objects.all()
            })
    else:
        html_content = """
            <div class="articles">
                <h2 style="text-align: center;">Top más likeados</h2>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones[:10]:
            texto = f"""
            <div class="article">
                <h2 style="text-transform: uppercase;">{ i.titulo }</h2>
                <h3>Likes: { i.me_gustas }</h3>
                <a href="/home/categoria/{i.categoria.descripcion_corta}">{ i.categoria.descripcion_corta } <br></a> 
                <p>Autor: <a href="/perfil/{i.user}">{i.user}</a></p>
                <p>Fecha: { i.fecha_creacion } </p>
                <button class="toggle-button" onclick="toggleContent('contenido-{i.id}')">Mostrar contenido</button>
                <a class="read-more" href="/crearpublicaciones/previsualizar/{ i.id }">IR A PAGINA</a>
                <div id="contenido-{i.id}" class="contenido"> {i.contenido_html} </div>
            </div>
            """
            html_content += texto  # Esta línea debería estar alineada correctamente dentro del bucle.

        html_content += "</div>"  # Añadido fuera del bucle.


        nuevo_reporte = Reporte.objects.create()

        nuevo_reporte.titulo = titulo
        nuevo_reporte.html_content = html_content
        nuevo_reporte.user = request.user.username
        nuevo_reporte.tipo = 'mas likeado'

        nuevo_reporte.save()
        return redirect('listaReportes')

@login_required
def porTiempo(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas

    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.all()


    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'redactadoPorTiempo.html', {
            'publicaciones': publicaciones, 
            'categorias': Categoria.objects.all()
            })
    
    else:
        html_content = """
            <div class="articles">
                <h2 style="text-align: center;">Publicaciones redactadas por tiempo</h2>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones:
            texto = f"""
            <div class="article">
                <h2 style="text-transform: uppercase;">{ i.titulo }</h2>
                <h3>Fecha: { i.fecha_creacion } </h3>
                <a href="/home/categoria/{i.categoria.descripcion_corta}">{ i.categoria.descripcion_corta } <br></a> 
                <p>Autor: <a href="/perfil/{i.user}">{i.user}</a></p>
                <button class="toggle-button" onclick="toggleContent('contenido-{i.id}')">Mostrar contenido</button>
                <a class="read-more" href="/crearpublicaciones/previsualizar/{ i.id }">IR A PAGINA</a>
                <div id="contenido-{i.id}" class="contenido"> {i.contenido_html} </div>
            </div>
            """
            html_content += texto  # Esta línea debería estar alineada correctamente dentro del bucle.

        html_content += "</div>"  # Añadido fuera del bucle.


        nuevo_reporte = Reporte.objects.create()

        nuevo_reporte.titulo = titulo
        nuevo_reporte.html_content = html_content
        nuevo_reporte.user = request.user.username
        nuevo_reporte.tipo = 'redactado por tiempo'

        nuevo_reporte.save()
        return redirect('listaReportes')

@login_required
def listaReportes(request):
    reportes = Reporte.objects.all()
    return render(request, 'lista_reportes.html', {
        'reportes': list(reportes.order_by('-fecha_creacion'))
        })

@login_required
def visualizarReporte(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)

    return render(request, 'visualizar_reporte.html', {
        'reporte': reporte
        })

@login_required
def eliminarReporte(request, reporte_id):
    reporte = Reporte.objects.get(id=reporte_id)
    reporte.delete()

    reportes = Reporte.objects.all()
    return redirect('listaReportes')

@login_required
def dashboard(request):
    nro_publicado= Publicacion.objects.filter(estado="publicado")
    nro_revision= Publicacion.objects.filter(estado="borrador")
    mas_interactuado = Publicacion.objects.all().order_by('-me_gustas')
    return render(request, 'dashboard.html', {
        'nro_publicado': len(nro_publicado),
        'nro_revision': len(nro_revision),
        'mas_interactuado': mas_interactuado[0],
        'publicaciones': nro_revision
    })