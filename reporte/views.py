from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from crearpublicaciones.models import *
from login.models import *
from .models import *
from login.models import *
from datetime import timedelta
from login.utils import *


# Create your views here.

@login_required
def masVistos(request):
    """
    Vista para mostrar las publicaciones más vistas basadas en los filtros especificados (rango de fechas y categorías).
    Si el método de la solicitud es POST, genera un informe con las 10 publicaciones más vistas.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con una lista de las publicaciones más vistas o una redirección a 'listaReportes' tras la creación del informe.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
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
def inactivosPorFecha(request):
    """
    Vista para mostrar las publicaciones inactivas basadas en los filtros especificados (rango de fechas y categorías).
    Si el método de la solicitud es POST, genera un informe con las 10 publicaciones más vistas.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con una lista de las publicaciones más vistas o una redirección a 'listaReportes' tras la creación del informe.
    """
    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas

    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.all()
    publicaciones = Publicacion.objects.filter(estado='inactivo').order_by('-fecha_publicacion')


    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'inactivosPorFecha.html', {
            'publicaciones': list(publicaciones), 
            'categorias': Categoria.objects.all()
            })
    
    else:
        html_content = """
            <div class="articles">
                <h2 style="text-align: center;">Listado de Inactivos por Tiempo</h2>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones:
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
        nuevo_reporte.tipo = 'articulos inactivados por tiempo'

        nuevo_reporte.save()
        return redirect('listaReportes')

@login_required
def masLikeados(request):
    """
    Vista para mostrar las publicaciones con más likes basadas en los filtros especificados (rango de fechas y categorías).
    Si el método de la solicitud es POST, genera un informe con las 10 publicaciones con más likes.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con una lista de las publicaciones con más likes o una redirección a 'listaReportes' tras la creación del informe.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
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
    """
    Vista para mostrar las publicaciones redactadas en un rango de tiempo especificado y basadas en categorías seleccionadas.
    Si el método de la solicitud es POST, genera un informe con todas las publicaciones redactadas en el tiempo especificado.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con una lista de publicaciones por tiempo o una redirección a 'listaReportes' tras la creación del informe.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
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
        html_content = f"""
            <div class="articles">
                <h2 style="text-align: center;">Publicaciones redactadas por tiempo</h2>
                <h3 style="text-align: center;">Del {start_date} al {end_date}: {len(publicaciones)} publicación/es</h3>
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
def publicadoPorTiempo(request):
    """
    Vista para mostrar las publicaciones publicadas en un rango de tiempo especificado y basadas en categorías seleccionadas.
    Si el método de la solicitud es POST, genera un informe con todas las publicaciones publicadas en el tiempo especificado.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con una lista de publicaciones publicadas en el tiempo o una redirección a 'listaReportes' tras la creación del informe.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas

    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.filter(estado='publicado').order_by('-fecha_publicacion')

    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_publicacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'publicadoPorTiempo.html', {
            'publicaciones': publicaciones, 
            'categorias': Categoria.objects.all()
            })
    
    else:
        html_content = f"""
            <div class="articles">
                <h2 style="text-align: center;">Artículos publicados por tiempo</h2>
                <h3 style="text-align: center;">Del {start_date} al {end_date}: {len(publicaciones)} publicación/es</h3>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones:
            texto = f"""
            <div class="article">
                <h2 style="text-transform: uppercase;">{ i.titulo }</h2>
                <h3>Fecha publicacion: { i.fecha_publicacion} </h3>
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
        nuevo_reporte.tipo = 'publicado por tiempo'

        nuevo_reporte.save()
        return redirect('listaReportes')

@login_required
def promedioRevision(request):
    """
    Vista para calcular el promedio de tiempo en revisión de las publicaciones en un rango de tiempo especificado y categorías seleccionadas.
    Si el método de la solicitud es POST, genera un informe mostrando el promedio de tiempo en revisión de las publicaciones en el tiempo especificado.

    Args:
        request (HttpRequest): La solicitud HTTP que contiene parámetros GET opcionales: 'start_date', 'end_date', 'categories'.

    Returns:
        HttpResponse: HTML renderizado con el promedio de tiempo de revisión o una redirección a 'listaReportes' tras la creación del informe.
    """


    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    start_date = request.GET.get('start-date')
    end_date = request.GET.get('end-date')
    categories = request.GET.getlist('categories')  # Esto obtiene una lista de categorías seleccionadas
    
    # Realiza la consulta a la base de datos utilizando los filtros obtenidos
    publicaciones = Publicacion.objects.filter(estado='publicado')
    publicaciones = publicaciones.order_by('-fecha_creacion')

    if start_date and end_date:
        publicaciones = publicaciones.filter(fecha_creacion__range=[start_date, end_date])

    if categories:
        publicaciones = publicaciones.filter(categoria__descripcion_corta__in=categories)

    if request.method == 'GET':

        return render(request, 'promedio_publicacion.html', {
            'publicaciones': list(publicaciones.order_by('-fecha_creacion')), 
            'categorias': Categoria.objects.all()
            })
    else:
        promedio = timedelta() 
        for i in publicaciones:
            promedio += i.fecha_publicacion - i.fecha_creacion

        if len(publicaciones) == 0:
            return render(request, 'promedio_publicacion.html', {
                'publicaciones': list(publicaciones.order_by('-fecha_creacion')), 
                'categorias': Categoria.objects.all()
            })
            
        
        promedio = promedio / len(publicaciones)

        dias = promedio.days
        segundos_totales = promedio.seconds
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60


        html_content = f"""
            <div class="articles">
                <h2 style="text-align: center;">Promedio de revision de los siguientes artículos</h2>
                <h3 style="text-align: center;"> {dias} días {horas} horas {minutos} minutos y {segundos} segundos</h3>
                <br><hr>
            </div>
        """
        titulo = request.POST.get('titulo')
        
        for i in publicaciones[:10]:
            en_revision = i.fecha_publicacion - i.fecha_creacion

            dias = en_revision.days
            segundos_totales = en_revision.seconds
            horas = segundos_totales // 3600
            minutos = (segundos_totales % 3600) // 60
            segundos = segundos_totales % 60

            texto = f"""
            <div class="article">
                <h2 style="text-transform: uppercase;">{ i.titulo }</h2>
                <h3>Likes: { i.me_gustas }</h3>
                <a href="/home/categoria/{i.categoria.descripcion_corta}">{ i.categoria.descripcion_corta } <br></a> 
                <p>Autor: <a href="/perfil/{i.user}">{i.user}</a></p>
                <h3>Tiempo en revisión: {dias} días {horas} horas {minutos} minutos y {segundos} segundos</h3>
                <p>Fecha creacion: { i.fecha_creacion } </p>
                <p>Fecha publicacion: { i.fecha_publicacion } </p>
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
        nuevo_reporte.tipo = 'tiempo de revision'

        nuevo_reporte.save()
        return redirect('listaReportes')


@login_required
def listaReportes(request):
    """
    Vista para mostrar la lista de reportes generados en el sistema ordenados por la fecha de creación.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: HTML renderizado con una lista de reportes ordenados.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    reportes = Reporte.objects.all()
    return render(request, 'lista_reportes.html', {
        'reportes': list(reportes.order_by('-fecha_creacion'))
        })

@login_required
def visualizarReporte(request, reporte_id):
    """
    Vista para mostrar el contenido de un reporte específico basado en su ID.

    Args:
        request (HttpRequest): La solicitud HTTP.
        reporte_id (int): El ID del reporte a visualizar.

    Returns:
        HttpResponse: HTML renderizado con el contenido del reporte seleccionado.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    reporte = Reporte.objects.get(id=reporte_id)

    return render(request, 'visualizar_reporte.html', {
        'reporte': reporte
        })

@login_required
def eliminarReporte(request, reporte_id):
    """
    Vista para eliminar un reporte basado en su ID.

    Args:
        request (HttpRequest): La solicitud HTTP.
        reporte_id (int): El ID del reporte a eliminar.

    Returns:
        HttpResponse: Redirección a la lista de reportes después de la eliminación.
    """

    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    reporte = Reporte.objects.get(id=reporte_id)
    reporte.delete()

    reportes = Reporte.objects.all()
    return redirect('listaReportes')

@login_required
def dashboard(request):
    """
    Vista del tablero que muestra estadísticas sobre las publicaciones y roles en el sistema.

    Args:
        request (HttpRequest): La solicitud HTTP.

    Returns:
        HttpResponse: HTML renderizado con estadísticas sobre publicaciones y usuarios según sus roles.
    """
    if not verificar_permisos_admin(request, ['acceder reportes']):
        return render(request, 'sin_permiso.html')

    nro_publicado = Publicacion.objects.filter(estado="publicado")
    nro_borrador = Publicacion.objects.filter(estado="borrador")
    nro_revision = Publicacion.objects.filter(estado="revision")
    nro_rechazado = Publicacion.objects.filter(estado="rechazado")

    suscriptor = Rol.objects.get(nombre='Suscriptor')
    nro_suscriptor= UsuarioRolCategoria.objects.filter(rol=suscriptor)

    editor = Rol.objects.get(nombre='Editor')
    nro_editor= UsuarioRolCategoria.objects.filter(rol=editor)

    publicador = Rol.objects.get(nombre='Publicador')
    nro_publicador= UsuarioRolCategoria.objects.filter(rol=publicador)

    autor = Rol.objects.get(nombre='Autor')
    nro_autor = UsuarioRolCategoria.objects.filter(rol=autor)

    administrador = Rol.objects.get(nombre='Administrador')
    nro_administrador = UsuarioRolCategoria.objects.filter(rol=administrador)
    
    return render(request, 'dashboard.html', {
        'nro_publicado': len(nro_publicado),
        'nro_revision': len(nro_revision),
        'nro_borrador': len(nro_borrador),
        'nro_rechazado': len(nro_rechazado),
        'publicaciones': Publicacion.objects.exclude(estado="publicado"),

        'nro_suscriptor': len(nro_suscriptor),
        'nro_editor': len(nro_editor),
        'nro_publicador': len(nro_publicador),
        'nro_autor': len(nro_autor),
        'nro_administrador': len(nro_administrador)
    })