from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Modelo de Tienda
class Tienda(models.Model):
    #Al realizar las migrate, se crea las tablas en la base de datos con estos modelos
    #Recordar utilizar en settings.py la configuracion para la base de datos que se va a utilizar
    #para majenar por usuario /En el proyecto usaremos el usuario general
    """Modelo OPP Clase que representa una tienda creada por el usuario general en proyecto."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100, help_text="Nombre de la tienda")
    logo = models.ImageField(upload_to='tiendas/', null=True , blank=True)
    eslogan = models.TextField(null=True, blank=True)
    ubicacion = models.TextField(null=False, help_text="Provincia Canton Distrito Pueblo")
    fecha_creada = models.DateTimeField(default=timezone.now)
    ##propietario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="tiendas",
      #                               help_text="Usuario propietario de la tienda")

    def __str__(self):
        strM = f"{self.nombre}  Ubicacion: {self.ubicacion}"
        return strM


# Modelo de Producto
class Producto(models.Model):
    
    """Modelo que representa un producto dentro de una tienda."""
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name="productos", help_text="Tienda a la que pertenece el producto")
    nombre = models.CharField(max_length=100, help_text="Nombre del producto")
    descripcion = models.TextField(blank=True, null=True, help_text="Descripción del producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, help_text="Precio del producto")
    stock = models.PositiveIntegerField(default=0, help_text="Cantidad disponible en stock")
    estrellas = models.PositiveIntegerField(default=0, help_text="Estrellas del producto")

    def __str__(self):
        return f"{self.nombre} - {self.tienda.nombre}"


# Modelo de Carrito
class Carrito(models.Model):
    """Modelo que representa el carrito de compras de un usuario."""
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito",
                                   help_text="Usuario propietario del carrito")
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name="carritos",
                               null=True, blank=True, help_text="Tienda asociada al carrito actual")
    productos = models.ManyToManyField(Producto, through="CarritoProducto", help_text="Productos en el carrito")
    
    monto = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


# Modelo intermedio para Carrito y Producto
class CarritoProducto(models.Model):
    """Modelo intermedio para manejar la cantidad de productos en un carrito."""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, help_text="Carrito asociado")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, help_text="Producto asociado")
    cantidad = models.PositiveIntegerField(default=1, help_text="Cantidad del producto en el carrito")

    class Meta:
        unique_together = ('carrito', 'producto')  # Evitar duplicados del mismo producto en el carrito


# Modelo de Pedido
class Pedido(models.Model):
    """Modelo que representa un pedido confirmado."""
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="pedidos",
                                help_text="Usuario que realiza el pedido")
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name="pedidos",
                               help_text="Tienda de donde provienen los productos del pedido")
    productos = models.ManyToManyField(Producto, through="PedidoProducto", help_text="Productos del pedido")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Monto total del pedido")
    confirmado = models.BooleanField(default=False, help_text="Estado de confirmación del pedido")
    fecha = models.DateTimeField(auto_now_add=True, help_text="Fecha y hora del pedido")

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.username}"


# Modelo intermedio para Pedido y Producto
class PedidoProducto(models.Model):
    """Modelo intermedio para manejar la cantidad de productos en un pedido."""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, help_text="Pedido asociado")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, help_text="Producto asociado")
    cantidad = models.PositiveIntegerField(help_text="Cantidad del producto en el pedido")

    def __str__(self):
        return f"{self.producto.nombre} (x{self.cantidad}) en Pedido #{self.pedido.id}"
