from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator #validaciones
from django.utils.text import slugify #urls seguras, filtro de plantilla convierte texto en una cadena unica y legible para la URLs
"""
Notas
    slugify #urls seguras, filtro de plantilla convierte texto en una cadena unica y legible para la URLs
        title = "como crear urls amigables"
        slug = slugify(title)
        print(slug)
        : como-crear-urls-amigables
Preguntas:
    Para que el atributo slug en tiendas y categoria
    como trabajo esto:  on_delete=models.SET_NULL
"""

from PIL import Image #comprensión de Imagenes , 

# Modelo de Provincias para ubicación jerárquica
class Provincia(models.Model):
    """
    Modelo para almacenar las provincias del país
    Permite una selección jerárquica de ubicación
    """
    nombre = models.CharField(max_length=100, unique=True) #solo tendra el id y nombre
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name_plural = "Provincias"
        ordering = ['nombre']

class Canton(models.Model):
    """
    Modelo para almacenar los cantones de cada provincia
    """
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='cantones') 
    #related_name *related_name*: Este atributo define el nombre que se usará para la relación inversa desde el modelo X de vuelta al modelo Y.
    #con relacion de uno a muchos 
    
    
    def __str__(self):
        return f"{self.nombre} - {self.provincia}"
    
    class Meta:
        verbose_name_plural = "Cantones"
        unique_together = ('nombre', 'provincia')
        ordering = ['nombre']

class Distrito(models.Model):
    """
    Modelo para almacenar los distritos de cada cantón
    """
    nombre = models.CharField(max_length=100)
    canton = models.ForeignKey(Canton, on_delete=models.CASCADE, related_name='distritos')
    
    def __str__(self):
        return f"{self.nombre} - {self.canton}"
    
    class Meta:
        verbose_name_plural = "Distritos"
        unique_together = ('nombre', 'canton')
        ordering = ['nombre']
"""
class Pueblo(models.Model):
    
    #Modelo para almacenar los distritos de cada cantón
    
    nombre = models.CharField(max_length=100)
    distrito = models.ForeignKey(Distrito, on_delete=models.CASCADE, related_name='pueblos')
    def __str__(self):
        return f"{self.nombre} - {self.distrito}"
    
    class Meta:
        verbose_name_plural = "Distritos"
        unique_together = ('nombre', 'canton')
"""
#Productos
class Categoria(models.Model):
    """
    Modelo para categorías de productos
    Permite una clasificación organizada
    """
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, max_length=100) #los slug explicados para cadena de texto legible #name unico para la url
    descripcion = models.TextField(blank=True)

    def save(self, *args, **kwargs): #al guardar x se realiza este codigo interno
        """
        Genera automáticamente un slug único basado en el nombre
        """
        self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre'] #ordena evitar errores UnorderedObjectListWarning 

#Tiendas
class Tienda(models.Model):
    """
    Modelo de Tienda con todas las características requeridas
    """
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tiendas') #relacionamos con tiendas, y el usuario sera el logeado en el proyecto general para uso de proyectos
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=200) #name unico para la url
    eslogan = models.CharField(max_length=250, blank=True, null=True)
    logo = models.ImageField(upload_to='tiendas/logos/', blank=True, null=True)
    
    # Ubicación jerárquica
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    canton = models.ForeignKey(Canton, on_delete=models.SET_NULL, null=True)
    distrito = models.ForeignKey(Distrito, on_delete=models.SET_NULL, null=True)
    pueblo = models.CharField(max_length=100, blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estrellas = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])#usamos dec. para validar rango de estrellas
    total_ventas = models.IntegerField(default=0)
    total_dinero = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        """
        Genera automáticamente un slug único para la URL
        """
        try:
            if not self.slug:
                self.slug = slugify(self.nombre)
            
            # Redimensiona el logo si es necesario
            super().save(*args, **kwargs)
            
            if self.logo:#redimencionaos si hay logo
                self.resize_logo()
        except Exception as e:
            print(f"Error en guardar la tienda: {e}")
            
    def resize_logo(self, max_size=(300, 300)):
        """
        Redimensiona el logo de la tienda para optimizar espacio y rendimiento 
        """
        try:
            img = Image.open(self.logo.path)
            img.thumbnail(max_size)
            img.save(self.logo.path)
        except Exception as e:
            print(f"Ha ocurrido un error {e}")

    def calcular_estrellas(self):
        """
        Calcula el promedio de estrellas basado en las calificaciones de productos, 
        
        cambiar logica por alteraciones del rating
            seguridad
        """
        try:
            productos = self.productos.all() #related_name general : productos : se menciona a la hora de crear el atributo del modelo
            if productos:
                promedio = sum(p.estrellas for p in productos) / len(productos) #encontramos el promedio mediante la formula
                self.estrellas = round(promedio, 2) #redondeamos entero
                self.save() #guardamos las estrellas del producto segun la cantidad de
        except Exception as e:
            print(f"Error en el calculo de estrellas: {e}")
    
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Tiendas"
        ordering = ['nombre']



class Producto(models.Model):
    """
    Modelo de Producto con características detalladas
    """
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    nombre = models.CharField(max_length=250)
    
    slug = models.SlugField(unique=True, max_length=250) #url unica del slug
    
    # Máximo 3 fotos con redimensionamiento : funcion en Tienda
    foto1 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto2 = models.ImageField(upload_to='productos/', blank=True, null=True)
    foto3 = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    detalles = models.TextField()
    precio = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    
    estrellas = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """
        Genera slug y redimensiona imágenes
        """
        if not self.slug:
            self.slug = slugify(self.nombre)
        
        super().save(*args, **kwargs)
        
        # Redimensiona imágenes
        self.resize_images()


    def resize_images(self, max_size=(800, 600)):
        """
        Redimensiona y optimiza imágenes de los productos
        """
        try:
            for field_name in ['foto1', 'foto2', 'foto3']:
                foto = getattr(self, field_name)
                if foto:
                    img = Image.open(foto.path)
                    img.thumbnail(max_size)
                    img.save(foto.path, optimize=True, quality=85)
        except Exception as e:
            print(f"Error en redimensionar imagenes: {e}")
            
    def __str__(self):
        return f"{self.nombre} - {self.tienda.nombre}"

    class Meta:
        verbose_name_plural = "Productos"
        unique_together = ('tienda', 'nombre')
        ordering = ['nombre']

class Carrito(models.Model):
    """
    Modelo de Carrito por usuario y tienda
    Mantiene estado persistente entre sesiones
    """
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    ultima_actualizacion = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Carrito de {self.usuario.username} - {self.tienda.nombre}"

    class Meta:
        unique_together = ('usuario', 'tienda')
        verbose_name_plural = "Carritos"
        ordering = ['-fecha_creacion']

class ItemCarrito(models.Model):
    """
    Productos dentro del carrito con control de cantidad, modelado objetos, o bien las listas por tienda
    """
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        """
        Calcula el subtotal del item
        """
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"

    class Meta:
        unique_together = ('carrito', 'producto') #unica comunicacion
        verbose_name_plural = "Items de Carrito"
        ordering = ['producto']