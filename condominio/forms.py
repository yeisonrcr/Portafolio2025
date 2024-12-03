from django import forms
from .models import PerfilUsuario, RegistroVisitas, RegistroAutomoviles, RegistroMascotas, RegistroReportes


class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ['integrantes_permanente', 'placas_permanentes']

class RegistroVisitasForm(forms.ModelForm):
    class Meta:
        model = RegistroVisitas
        fields = ['personas_visitantes', 'placas_autorizadas']

class RegistroAutomovilesForm(forms.ModelForm):
    class Meta:
        model = RegistroAutomoviles
        fields = ['auto', 'imagen', 'caracteristicas', 'placa']

class RegistroMascotasForm(forms.ModelForm):
    class Meta:
        model = RegistroMascotas
        fields = ['nombre', 'foto', 'caracteristicas']

class RegistroReportesForm(forms.ModelForm):
    class Meta:
        model = RegistroReportes
        fields = ['reporte']