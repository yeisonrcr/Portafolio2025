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
    CrearProductoView,CarritoView
    
    # Otras vistas que puedan ser necesarias
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
    path('carrito/', CarritoView.as_view(), name='carrito'),
]

# Configuración para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)