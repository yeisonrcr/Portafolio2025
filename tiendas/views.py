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
from .models import Tienda, Producto, Categoria, Carrito, ItemCarrito, Provincia
from .forms import TiendaForm, ProductoForm, CarritoForm

from django.core.paginator import Paginator
#manejar paginación de tablas a 10 campos, rendimiento.

class TiendaListView(ListView):
    """
    Vista para listar todas las tiendas disponibles
    Implementa búsqueda y filtrado
    """
    model = Tienda
    #template_name = 'tienda_list.html'
    context_object_name = 'tiendas' #relaciones configuradas
    paginate_by = 10  # Paginación de 10 tiendas

    def get_queryset(self):
        """
        Método para implementar búsqueda y filtrado de tiendas
        """
        queryset = Tienda.objects.all()
        try:
            query = self.request.GET.get('q')
            if query: #si hay un dato de x en y 
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
        
        # Búsqueda por nombre o ubicación
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto
        """
        context = super().get_context_data(**kwargs)
        context['provincias'] = Provincia.objects.all()
        return context





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
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(provincia__nombre__icontains=query) |
                Q(canton__nombre__icontains=query)
            )
        
        provincia = self.request.GET.get('provincia')
        if provincia:
            queryset = queryset.filter(provincia__nombre=provincia)
        
        return queryset

    def get_context_data(self, **kwargs):
        """
        Añade información adicional al contexto
        """
        context = super().get_context_data(**kwargs)
        context['provincias'] = Provincia.objects.all()
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


class CarritoView(LoginRequiredMixin, View):
    """
    Vista para gestionar el carrito de compras
    Permite modificar y eliminar productos
    """
    template_name = 'tiendas/carrito.html'

    def get(self, request):
        """
        Muestra los carritos del usuario
        """
        carritos = Carrito.objects.filter(usuario=request.user)
        return render(request, self.template_name, {'carritos': carritos})

    def post(self, request):
        
        """
        Procesa modificaciones del carrito
        """
        # Lógica para actualizar cantidades o eliminar items
        # Implementación detallada según requerimientos específicos



class CrearProductoView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    Vista para crear productos en una tienda
    Solo el propietario de la tienda puede agregar productos
    """
    model = Producto
    form_class = ProductoForm
    #template_name = 'ecommerce/crear_producto.html'

    def test_func(self):
        """
        Verifica que solo el propietario de la tienda pueda agregar productos
        """
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk'])
        return self.request.user == tienda.propietario

    def form_valid(self, form):
        """
        Asigna la tienda al producto
        """
        tienda = get_object_or_404(Tienda, pk=self.kwargs['tienda_pk'])
        form.instance.tienda = tienda
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirige a la lista de productos de la tienda
        """
        return reverse_lazy('tienda_detail', kwargs={'pk': self.kwargs['tienda_pk']})