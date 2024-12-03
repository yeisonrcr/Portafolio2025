from django.contrib import admin
from .models import *
# Register your models here.


#forma basica de registrar las tablas de esta app em el admin DJANGO 
admin.site.register(RegistroVisitas)
admin.site.register(RegistroAutomoviles)
admin.site.register(RegistroMascotas)
admin.site.register(RegistroReportes)


#segunda forma
@admin.register(PerfilUsuario)
class RegistroVisitasAdmin(admin.ModelAdmin):
    list_display = ("usuario", "casa",)
    search_fields = ("usuaurio_username","casa")
    