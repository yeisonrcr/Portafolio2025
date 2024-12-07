#Utilizaré vistas basadas en clases para aprovechar la herencia y mantener un código más organizado.
#vistas por defecto
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, View
)

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin #mixins utilizados, explicación en el archivo info
from django.urls import reverse_lazy #definir URLs por adelantado 

#consultas complejas a la base de datos combinar usando operadores logicos y demas
from django.db.models import Q 

from django.shortcuts import get_object_or_404, redirect, render #rendings
from django.contrib import messages #messager front

#mis archivos
from .models import Tienda, Producto, Categoria, Carrito, ItemCarrito, Provincia, Canton, Distrito
from .forms import TiendaForm, ProductoForm, CarritoForm

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#manejar paginación de tablas a 10 campos, rendimiento.


#funciones api
from django.http import JsonResponse

def get_cantones(request): 
    provincia_id = request.GET.get('provincia_id') 
    cantones = Canton.objects.filter(provincia_id=provincia_id).order_by('nombre') 
    return JsonResponse(list(cantones.values('id', 'nombre')), safe=False) 

def get_distritos(request): 
    canton_id = request.GET.get('canton_id') 
    distritos = Distrito.objects.filter(canton_id=canton_id).order_by('nombre') 
    return JsonResponse(list(distritos.values('id', 'nombre')), safe=False)



class TiendaListView(ListView):
    """
    Vista para listar todas las tiendas disponibles
    Implementa búsqueda y filtrado
    """
    model = Tienda
    context_object_name = 'tiendas'
    paginate_by = 10  # Paginación de 10 tiendas

    def get_queryset(self):
        """
        Método para implementar búsqueda y filtrado de tiendas
        """
        queryset = Tienda.objects.all()

        try:
            # Búsqueda por términos
            query = self.request.GET.get('q')
            if query:
                queryset = queryset.filter(
                    Q(nombre__icontains=query) |
                    Q(provincia__nombre__icontains=query) |
                    Q(canton__nombre__icontains=query)
                )

            # Filtrado por provincia
            provincia = self.request.GET.get('provincia')
            if provincia:
                queryset = queryset.filter(provincia__nombre=provincia)

        except Exception as e:
            raise e

        # Asegurar orden antes de retornar
        return queryset.order_by('-fecha_creacion')  # Ordenar por fecha de creación descendente

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto
        """
        context = super().get_context_data(**kwargs)
        context['provincias'] = Provincia.objects.all()  # Listado de provincias para filtros
        return context

class TiendaDetailView(DetailView):
    """
    Vista de detalle para una tienda específica
    Muestra productos de la tienda con paginación
    """
    model = Tienda
    #template_name = 'ecommerce/tienda_detail.html'
    context_object_name = 'tienda'
    

    def get_context_data(self, **kwargs):
        """
        Añade productos de la tienda con filtrado y paginación
        """
        context = super().get_context_data(**kwargs)
        try:
            
            # Obtener productos de la tienda
            productos = self.object.productos.all()
            
            # Filtrado por categoría
            categoria = self.request.GET.get('categoria')
            if categoria:
                productos = productos.filter(categoria__slug=categoria)
            
            # Búsqueda de productos
            query = self.request.GET.get('q')
            if query:
                productos = productos.filter(
                    Q(nombre__icontains=query) | 
                    Q(detalles__icontains=query)
                )
            
            # Paginación
            paginator = Paginator(productos, 10)  # 10 productos por página
            page_number = self.request.GET.get('page')
            context['productos'] = paginator.get_page(page_number)
            
            # Categorías de la tienda
            context['categorias'] = Categoria.objects.filter(
                producto__tienda=self.object
            ).distinct()
            
            

        except Exception as e:
            raise e
                
        return context

class ProductoDetailView(DetailView):
    """
    Vista de detalle para un producto específico
    Incluye lógica para agregar al carrito
    """
    model = Producto
    #template_name = 'ecommerce/producto_detail.html'
    context_object_name = 'producto'

    def get_context_data(self, **kwargs):
        """
        Añade formulario de carrito al contexto
        """
        context = super().get_context_data(**kwargs)
        try:
            #al seleccionar un producto
            context['carrito_form'] = CarritoForm(
                initial={'producto_id': self.object.id}
            )
        except Exception as e:
            raise e
            
        return context

    def post(self, request, *args, **kwargs):
        """
        Maneja la adición de productos al carrito
        """
        self.object = self.get_object()
        carrito_form = CarritoForm(request.POST)
        try:
            
            if carrito_form.is_valid():
                cantidad = carrito_form.cleaned_data['cantidad']
                
                # Obtener o crear carrito para esta tienda
                carrito, created = Carrito.objects.get_or_create(
                    usuario=request.user, 
                    tienda=self.object.tienda
                )
                
                # Verificar si el producto ya está en el carrito
                item_carrito, created = ItemCarrito.objects.get_or_create(
                    carrito=carrito,
                    producto=self.object,
                    defaults={
                        'cantidad': cantidad,
                        'precio_unitario': self.object.precio
                    }
                )
                
                # Si ya existe, actualizar cantidad
                if not created:
                    item_carrito.cantidad += cantidad
                    item_carrito.save()
                
                messages.success(request, f'Producto {self.object.nombre} agregado al carrito')
                return redirect('producto_detail', pk=self.object.pk)
            
        except Exception as e:
            raise e
        #GET
        return self.get(request, *args, **kwargs)

#Crear tienda, con el superuser logeado VERIFICAR LA SEGURIDAD QUE SOLO UN SUPERUSER PUEDE CREAR TIENDAS 
class CrearTiendaView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para crear una nueva tienda
    Solo accesible por superusuarios
    """
    model = Tienda
    form_class = TiendaForm
    #template_name = 'ecommerce/crear_tienda.html'
    success_url = reverse_lazy('tienda_list') #urls por adelantado 

    def test_func(self):
        """
        Verifica que solo superusuarios puedan crear tiendas
        """
        return self.request.user.is_superuser

    def form_valid(self, form):
        """
        Asigna el propietario de la tienda
        """
        form.instance.propietario = self.request.user
        return super().form_valid(form)

#agregar nuevo producto, y su seguridad
class CrearProductoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para crear productos en una tienda
    Solo el propietario de la tienda puede agregar productos
    """
    model = Producto #llamo el modelo
    form_class = ProductoForm #llamo el formulario para guardar datos al modelo
    #template_name = 'ecommerce/crear_producto.html' #utilizo el templates settings de django

    
    #seguridad
    def test_func(self):
        """
        Verifica que solo el propietario de la tienda pueda agregar productos
        """
        #control de agregado de productos
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk']) #obtengo la tienda para su relacion
        
        return self.request.user == tienda.propietario #retorno dueño del producto

    
    def form_valid(self, form):
        """
        Asigna la tienda al producto manual por seguridad objetos
        """
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk']) 
        print(str(tienda))
        
        form.instance.tienda = tienda
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirige a la lista de productos de la tienda
        """
        return reverse_lazy('tienda_detail', kwargs={'slug': self.object.tienda.slug})
        #return reverse_lazy('tienda_detail', kwargs={'slug': self.object.slug}) Estaba obteniendo el slug del producto y no el de la tienda
        
        #recordar que manejo slug para las url limpias pero puedes usar el PK de kwars para manejo como en los condominios
        
        #return reverse_lazy('tienda_detail', kwargs={'slug': self.kwargs['tienda_slug']})
        
        


"""
    Consideraciones Importantes

        Validación de Stock: En la vista, se valida que la cantidad no supere el stock disponible.
        Mensajes de Usuario: Se usan mensajes de Django para notificar acciones exitosas o errores.
        Seguridad: Solo el usuario propietario puede modificar su propio carrito.

"""

class CarritoView(LoginRequiredMixin, View):
    """
    Vista para gestionar el carrito de compras
    Permite varias funciones
    """
    template_name = 'tiendas/carrito.html' #declaro la template que voy a usar
    items_por_pagina = 10  # Configuración de paginación

    def get(self, request): # al hacer una consulta
        """
        Muestra el carrito del usuario, con varios carritos, y cada carrito con varios items se maneja orientado a objetos en los models 
            Se utiliza funciones por defecto Django
                Carrito
                    ItemCarrito
        
        carritos = Carrito.objects.filter(usuario=request.user)
        #envio con normalidad para mas ordenado
        return render(request, self.template_name, {'carritos': carritos})
        """
        # Obtener todos los carritos del usuario
        carritos = Carrito.objects.filter(usuario=request.user)
        
        # Lista para almacenar carritos paginados
        carritos_paginados = []
        
        for carrito in carritos:
            # Obtener items del carrito
            items = carrito.items.all()
            
            # Configurar paginación para los items de cada carrito
            paginator = Paginator(items, self.items_por_pagina)
            
            # Obtener el número de página de la solicitud
            page = request.GET.get(f'page_carrito_{carrito.id}', 1)
            
            try:
                # Obtener la página específica de items
                items_pagina = paginator.page(page)
            except PageNotAnInteger:
                # Si no es un número, mostrar la primera página
                items_pagina = paginator.page(1)
            except EmptyPage:
                # Si la página está fuera de rango, mostrar la última página
                items_pagina = paginator.page(paginator.num_pages)
            
            # Crear un diccionario con el carrito y sus items paginados
            carrito_paginado = {
                'carrito': carrito,
                'items': items_pagina,
                'total_paginas': paginator.num_pages,
                'pagina_actual': items_pagina.number
            }
            
            carritos_paginados.append(carrito_paginado)
        
        return render(request, self.template_name, {
            'carritos_paginados': carritos_paginados
        })



    #funciones post request http
    def post(self, request):
        """
        Procesa modificaciones del carrito
        """
        try:
            # Actualizar cantidad de un ítemCarrito del carrito
            if 'actualizar_cantidad' in request.POST:
                item_id = request.POST.get('item_id')#obtengo el item 
                nueva_cantidad = request.POST.get('cantidad') #obtengo la nueva cantidad por el usuario en el formulario
                
                try:
                    item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user) # manejo de errores, tato de 
                    #Obtengo el item con el acceso debido
                    #seguridad para produccion escalable
                    
                    # Validar que la cantidad no exceda el stock
                    producto = item.producto
                    if int(nueva_cantidad) <= producto.stock:#validamos la cantidad de los productos 
                        item.cantidad = nueva_cantidad # si cambiamos la cantidad del item
                        item.save() #guardo lo nuevo al item
                        messages.success(request, 'Cantidad actualizada correctamente') #manejamos msj por ahora
                    else:
                        messages.error(request, f'Solo hay {producto.stock} unidades disponibles')
                
                except ItemCarrito.DoesNotExist:
                    messages.error(request, 'El ítem no existe')
            
            # Vaciar carrito completo
            elif 'vaciar_carrito' in request.POST:
                carrito_id = request.POST.get('carrito_id')
                try:
                    #manejo carritos y items en cada carrito por usuarios logeados
                    carrito = Carrito.objects.get(id=carrito_id, usuario=request.user) #envio id y usuario (con los mixins)
                    carrito.items.all().delete() #elimino los items en este carrito
                    messages.success(request, 'Carrito vaciado correctamente')
                except Carrito.DoesNotExist:
                    messages.error(request, 'El carrito no existe')
            
            # Eliminar ítem específico
            elif 'eliminar_item' in request.POST:
                #obtengo el item e intento eliminarlo
                item_id = request.POST.get('item_id')
                try:
                    item = ItemCarrito.objects.get(id=item_id, carrito__usuario=request.user) #envio peticion a la base de datos de los items agregados al carrito ID, (envio mixins id, y user)
                    item.delete() #elimino el item 
                    messages.success(request, 'Producto eliminado del carrito')
                except ItemCarrito.DoesNotExist:
                    messages.error(request, 'El ítem no existe') #si no es portque no hay nada aca
        
        except Exception as e:
            messages.error(request, f'Error al procesar el carrito: {str(e)}')
        return redirect('carrito') #retorno carrito





