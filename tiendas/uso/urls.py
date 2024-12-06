from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    # Vistas de Tiendas
    TiendaListView, 
    TiendaDetailView, 
    CrearTiendaView,
    
    # Vistas de Productos
    ProductoDetailView,
    CrearProductoView,CarritoView,
    
    # New cart and order views
    CarritoView, OrdenListView, OrdenDetailView
)
# Definición de patrones de URL
urlpatterns = [
    # URLs para Tiendas
    path('', TiendaListView.as_view(), name='tienda_list'),
    path('tienda/<slug:slug>/', TiendaDetailView.as_view(), name='tienda_detail'),
    path('tienda/crear/', CrearTiendaView.as_view(), name='crear_tienda'),
    
    # URLs para Productos
    path('producto/<slug:slug>/', ProductoDetailView.as_view(), name='producto_detail'),
    path('tienda/<int:tienda_pk>/producto/crear/', CrearProductoView.as_view(), name='crear_producto'),
    
    # URLs adicionales que podríamos necesitar
    
    # Cart URLs
    path('carrito/', CarritoView.as_view(), name='carrito'),
    
    # Order URLs
    path('ordenes/', OrdenListView.as_view(), name='orden_list'),
    path('orden/<int:pk>/', OrdenDetailView.as_view(), name='orden_detalle'),
    
]

# Configuración para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)