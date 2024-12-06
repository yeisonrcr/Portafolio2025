from django import forms
from django.core.exceptions import ValidationError #utilizaremos validadores 
from .models import Tienda, Producto, Categoria, Provincia, Canton, Distrito

class ProvinciaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Provincias
    Hereda de ModelForm para validación automática
    """
    class Meta:
        model = Provincia
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class CantonForm(forms.ModelForm):
    """
    Formulario para creación y edición de Cantones
    Incluye validación de provincia
    """
    class Meta:
        model = Canton
        fields = ['nombre', 'provincia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'})
        }

class DistritoForm(forms.ModelForm):
    """
    Formulario para creación y edición de Distritos
    Validación de cantón incluida
    """
    class Meta:
        model = Distrito
        fields = ['nombre', 'canton']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'canton': forms.Select(attrs={'class': 'form-control'})
        }

class CategoriaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Categorías
    Incluye validación de nombre único
    """
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }

    def clean_nombre(self):
        """
        Validación personalizada para garantizar nombres únicos
        """
        nombre = self.cleaned_data['nombre']
        if Categoria.objects.filter(nombre__iexact=nombre).exists(): #si existe alguno
            raise ValidationError(f"Ya existe una categoría con este nombre: -> {nombre}") #se envia un error
        return nombre

class TiendaForm(forms.ModelForm):
    """
    Formulario para creación y edición de Tiendas
    Incluye validaciones y widgets personalizados
    """
    class Meta:
        model = Tienda
        fields = [
            'nombre', 'eslogan', 'logo', 
            'provincia', 'canton', 'distrito', 'pueblo'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'eslogan': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.FileInput(attrs={'class': 'form-control-file'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            'canton': forms.Select(attrs={'class': 'form-control'}),
            'distrito': forms.Select(attrs={'class': 'form-control'}),
            'pueblo': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_logo(self):
        """
        Validación de tamaño y tipo de imagen para logo
        """
        logo = self.cleaned_data.get('logo') #obtengo y guardo el logo en una variable
        try:
            if logo: #si hay logo
            # Limitar tamaño de imagen (5MB)
        
                if logo.size > 5 * 1024 * 1024: #es muy grande el logo
                    raise ValidationError("El tamaño del logo no debe exceder 5MB.")
                
                # Validar tipo de archivo
                valid_types = ['image/jpeg', 'image/png', 'image/gif']
                if logo.content_type not in valid_types:
                    raise ValidationError("Formato de imagen no válido. Use JPEG, PNG o GIF.")
                
        except Exception as e:
                raise e
                
        return logo

class ProductoForm(forms.ModelForm):
    """
    Formulario para creación y edición de Productos
    Validaciones exhaustivas para datos del producto
    """
    class Meta:
        model = Producto
        fields = [
            'nombre', 'categoria', 'detalles', 
            'precio', 'stock', 
            'foto1', 'foto2', 'foto3'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'detalles': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto1': forms.FileInput(attrs={'class': 'form-control-file'}),
            'foto2': forms.FileInput(attrs={'class': 'form-control-file'}),
            'foto3': forms.FileInput(attrs={'class': 'form-control-file'})
        }

    def clean_precio(self):
        """
        Validación de precio positivo
        """
        precio = self.cleaned_data['precio']
        try:
            if precio <= 0:
                raise ValidationError("El precio debe ser mayor a cero.")
        except Exception as e:
            raise e
            
        return precio

    def clean_stock(self):
        """
        Validación de stock positivo
        """
        stock = self.cleaned_data['stock']
        try:
            if stock < 0:
                raise ValidationError("El stock no puede ser negativo.")
        except Exception as e:
            raise e
        return stock

    def clean(self):
        """
        Validación de múltiples campos
        Limita a máximo 3 imágenes
        """
        #obtengo las imagenes del padre
        cleaned_data = super().clean()
        fotos = [cleaned_data.get('foto1'), 
                 cleaned_data.get('foto2'), 
                 cleaned_data.get('foto3')]
        
        # Validar tamaño de imágenes
        try:
            for foto in fotos:
                if foto:
                    if foto.size > 5 * 1024 * 1024:  # 5MB
                        raise ValidationError("Cada imagen no debe exceder 5MB.")
                    
                    valid_types = ['image/jpeg', 'image/png', 'image/gif']
                    if foto.content_type not in valid_types:
                        raise ValidationError("Solo se permiten imágenes JPEG, PNG o GIF.")
        except Exception as e:
            raise e

        return cleaned_data


class CarritoForm(forms.Form):
    producto_id = forms.IntegerField(widget=forms.HiddenInput())
    cantidad = forms.IntegerField(
        min_value=1, 
        initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'min': '1'
        }),
        label='Cantidad'
    )

    def clean_cantidad(self):
        cantidad = self.cleaned_data['cantidad']
        producto_id = self.cleaned_data.get('producto_id')
        
        if producto_id:
            try:
                producto = Producto.objects.get(id=producto_id)
                if cantidad > producto.stock:
                    raise forms.ValidationError(f'Solo hay {producto.stock} unidades disponibles')
            except Producto.DoesNotExist:
                raise forms.ValidationError('Producto no encontrado')
        
        return cantidad