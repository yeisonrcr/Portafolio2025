

# Crear los view por defecto de django   / Luego cambiamos las plantillas
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from .models import PerfilUsuario, RegistroVisitas, RegistroAutomoviles, RegistroMascotas, RegistroReportes
from .forms import PerfilUsuarioForm, RegistroVisitasForm, RegistroAutomovilesForm, RegistroMascotasForm , RegistroReportesForm

#decoradores
from django.contrib.auth.decorators import login_required #Decorador de login

#Se limpia el codigo en clases  y no en funciones mas atractivo y facil de mantener  (FALTANTE

from django.shortcuts import render, get_object_or_404, redirect
from .models import RegistroVisitas, RegistroAutomoviles, RegistroMascotas
from .forms import RegistroVisitasForm, RegistroAutomovilesForm, RegistroMascotasForm

#primer pagina para manejar funciones
def home(request, *args, **kwargs):
    return render (request, "gestion/home.html" , {"username": kwargs.get("pk")})


# Vistas para todos los perfiles de usuarios
def perfil_usuario_lista(request):
    #obtenemos todos los perfiles de usuario
    cursor = PerfilUsuario.objects.filter(usuario=request.user)
    
    return render(request, 'gestion/perfiles/perfil_usuario_lista.html', {'perfiles': cursor})


#vista un solo perfil de usuario
def perfil_usuario_detalle(request, pk):
    #obtenemos solo un perfil de usuario segun el PK
        #luego limpio este codigo con el kwargs por seguridad django y limpieza de crecimiento
    cursor = get_object_or_404(PerfilUsuario, pk=pk)
    return render(request, 'gestion/perfiles/perfil_usuario_detalle.html', {'perfil': cursor}) #renderizamos con el perfil del usuario ID escogido


#Registrar nuevo perfil
#crear el perfil de usuario logeado (Verificar logica) (FALTANTE MAL)
def perfil_usuario_nuevo(request):
    
    if request.method == "POST":#si es post
        form = PerfilUsuarioForm(request.POST) #obtenemos el formulario creado para registrar mi perfil
        if form.is_valid(): #si es valido los datos sin limpiar (FALTANTE)
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            return redirect('perfil_usuario_lista')
    else:
        form = PerfilUsuarioForm() #mostramos el formulario para registrar nuevo perfil (INTEGRANTES PERMANTENES NUEVO y PLACAS NUEVAS)
    return render(request, 'gestion/perfiles/perfil_usuario_editar.html', {'form': form}) #renderizamos a editar perfil usuario 


#Manejamos el pk por url otra forma para practicar
def perfil_usuario_editar(request, *args, **kwargs):
    #obtenemos el perfil del usuario o da error
        #get_object_or_404() explicado;    #funcion de atajo ir por un objeto a la base de datos o manejar error en caso de que no exista el pk 
    cursor = get_object_or_404(PerfilUsuario, pk=kwargs.get("pk"))
    
    if request.method == "POST": #si es enviando el formulario
        form = PerfilUsuarioForm(request.POST, instance=cursor) #datos del usuario se pueden limpiar mas adelante con cleaned_Data    la instance: son los datos del pk o id 
        if form.is_valid():
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            #retornamos el id del usuario por el pk
            return redirect('perfil_usuario_detalle', pk=cursor.pk) #redireccionamos al perfil actualizado con los datos nevos
    else:
        form = PerfilUsuarioForm(instance=cursor)
    return render(request, 'gestion/perfiles/perfil_usuario_editar.html', {'form': form})


#eliminar el perfil del usuario
def perfil_usuario_eliminar(request, pk):
    try:
        #obtenemos el pk de la url a eliminar
        perfil = get_object_or_404(PerfilUsuario, pk=pk)
        if perfil:
            perfil.delete()
            print("eliminado con exito")
        else:
            print("no se ha podido guardar")
    except Exception as e:
        print(str(e))

    return redirect('perfil_usuario_lista')


# Vistas para RegistroVisitas
def registro_visitas_lista(request):
    #visitas = RegistroVisitas.objects.all()#mostramos todas pero solo debe ser las que el usuario creo 
    
    cursor = RegistroVisitas.objects.filter(usuario=request.user)
    return render(request, 'gestion/visitas/registro_visitas_lista.html', {'visitas': cursor})

def registro_visitas_detalle(request, pk):
    
    cursor = get_object_or_404(RegistroVisitas, pk=pk)
    
    return render(request, 'gestion/visitas/registro_visitas_detalle.html', {'visita': cursor})

def registro_visitas_nuevo(request):
    if request.method == "POST":
        form = RegistroVisitasForm(request.POST)
        if form.is_valid():
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            return redirect('registro_visitas_detalle', pk=cursor.pk)
    else:
        form = RegistroVisitasForm()
    return render(request, 'gestion/visitas/registro_visitas_editar.html', {'form': form})

def registro_visitas_editar(request, pk):
    cursor = get_object_or_404(RegistroVisitas, pk=pk)
    if request.method == "POST":
        form = RegistroVisitasForm(request.POST, instance=cursor)
        if form.is_valid():
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            return redirect('registro_visitas_detalle', pk=cursor.pk)
    else:
        form = RegistroVisitasForm(instance=cursor)
    return render(request, 'gestion/visitas/registro_visitas_editar.html', {'form': form})

def registro_visitas_eliminar(request, pk):
    cursor = get_object_or_404(RegistroVisitas, pk=pk)
    cursor.delete()
    return redirect('registro_visitas_lista')




# Vistas para RegistroAutomoviles
def registro_automoviles_lista(request):
    #automoviles = RegistroAutomoviles.objects.all()

    cursor = RegistroAutomoviles.objects.filter(usuario=request.user)    
    return render(request, 'gestion/autos/registro_automoviles_lista.html', {'automoviles': cursor})

def registro_automoviles_detalle(request, pk):
    automovil = get_object_or_404(RegistroAutomoviles, pk=pk)
    return render(request, 'gestion/autos/registro_automoviles_detalle.html', {'automovil': automovil})

def registro_automoviles_nuevo(request):
    if request.method == "POST":
        form = RegistroAutomovilesForm(request.POST, request.FILES)
        if form.is_valid():
            
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            
            return redirect('registro_automoviles_detalle', pk=cursor.pk)
    else:
        form = RegistroAutomovilesForm()
    return render(request, 'gestion/autos/registro_automoviles_editar.html', {'form': form})

def registro_automoviles_editar(request, pk):
    cursor = get_object_or_404(RegistroAutomoviles, pk=pk)
    if request.method == "POST":
        form = RegistroAutomovilesForm(request.POST, request.FILES, instance=cursor)
        if form.is_valid():
            
            
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            
            return redirect('registro_automoviles_detalle', pk=cursor.pk)
    else:
        form = RegistroAutomovilesForm(instance=cursor)
    return render(request, 'gestion/autos/registro_automoviles_editar.html', {'form': form})

def registro_automoviles_eliminar(request, pk):
    cursor = get_object_or_404(RegistroAutomoviles, pk=pk)
    cursor.delete()
    return redirect('registro_automoviles_lista')



# Vistas para RegistroMascotas
def registro_mascotas_lista(request):
    #cursor = RegistroMascotas.objects.all()
    cursor = RegistroMascotas.objects.filter(usuario=request.user)
    return render(request, 'gestion/mascotas/registro_mascotas_lista.html', {'mascotas': cursor})

def registro_mascotas_detalle(request, pk):
    cursor = get_object_or_404(RegistroMascotas, pk=pk)
    return render(request, 'gestion/mascotas/registro_mascotas_detalle.html', {'mascota': cursor})

def registro_mascotas_nuevo(request):
    if request.method == "POST":
        form = RegistroMascotasForm(request.POST, request.FILES)
        if form.is_valid():
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            

            return redirect('registro_mascotas_detalle', pk=cursor.pk)
    else:
        form = RegistroMascotasForm()
    return render(request, 'gestion/mascotas/registro_mascotas_editar.html', {'form': form})

def registro_mascotas_editar(request, pk):
    cursor = get_object_or_404(RegistroMascotas, pk=pk)
    if request.method == "POST":
        form = RegistroMascotasForm(request.POST, request.FILES, instance=cursor)
        if form.is_valid():
            
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            
            return redirect('registro_mascotas_detalle', pk=cursor.pk)
    else:
        form = RegistroMascotasForm(instance=cursor)
    return render(request, 'gestion/mascotas/registro_mascotas_editar.html', {'form': form})

def registro_mascotas_eliminar(request, pk):
    cursor = get_object_or_404(RegistroMascotas, pk=pk)
    cursor.delete()
    return redirect('registro_mascotas_lista')


#CLEAN CODE para utilizar solo una carpeta de template 
#FALTANTE

# Vistas para REPORTES
def registro_reporte_lista(request):
    
    #solo los reportes hechos por  mi/usuario logeado
    cursor = RegistroReportes.objects.filter(usuario=request.user)
    return render(request, 'gestion/reportes/registro_reportes_lista.html', {'reportes': cursor})

def registro_reporte_detalle(request, pk):
    cursor = get_object_or_404(RegistroReportes, pk=pk)
    return render(request, 'gestion/reportes/registro_reportes_detalle.html', {'reporte': cursor})

def registro_reporte_nuevo(request):
    if request.method == "POST":
        form = RegistroReportesForm(request.POST, request.FILES)
        if form.is_valid():
            
            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            

            return redirect('reporte_detalle', pk=cursor.pk)
    else:
        form = RegistroReportesForm()
    return render(request, 'gestion/reportes/registro_reportes_editar.html', {'form': form})

def registro_reporte_editar(request, pk):
    cursor = get_object_or_404(RegistroReportes, pk=pk)
    if request.method == "POST":
        form = RegistroReportesForm(request.POST, request.FILES, instance=cursor)
        if form.is_valid():

            #nos aseguramos de incluir todos los datos necesarios para la base de datos 
            cursor = form.save(commit=False) #sin guardar en la base de datos pero guardado el formulario en una variable
            cursor.usuario = request.user #nos debemos asegurar de incluir el usuario para que se guarde la foreignKEY del usuario general
            cursor.save()#se guarda el nuevo perfil
            #esta correcto el formulario guardamos y guardamos la instancia
            
            
            return redirect('reporte_detalle', pk=cursor.pk)
    else:
        form = RegistroReportesForm(instance=cursor)
    return render(request, 'gestion/reportes/registro_reportes_editar.html', {'form': form})

def registro_reporte_eliminar(request, pk):
    cursor = get_object_or_404(RegistroReportes, pk=pk)
    cursor.delete()
    return redirect('reportes_lista')










