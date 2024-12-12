from django import forms
from django.contrib.auth.models import User
from . import models

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.Request
        fields=[ 'tipo' ,'vehicle_no',  'vehicle_mobile'  , 'vehicle_cliente'  ,'vehicle_name', 
                'vehicle_model','vehicle_brand','problem_description', 'distribuidorax','costAbonado', 'costTotal']

        widgets = {
            'problem_description':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        }
        
        
        
class DistribuidoraxForm(forms.ModelForm):
    class Meta:
        model = models.Request
        fields = ['distribuidorax']  # Agrega otros campos si es necesario

class AdminApproveRequestForm(forms.Form):
    costAbonado=forms.CharField()    
    stat=(('Consulta','Consulta') , ('Pendiente de investigar','Pendiente de investigar'),('Pendiente de enviar','Pendiente de enviar'),('Enviado','Enviado'))
    status=forms.ChoiceField( choices=stat)
    
    estad=(('Consulta','Consulta'),('Abonado','Abonado'),('Cotizado','Cotizado'),('Pagado','Pagado'))
    estado=forms.ChoiceField( choices=estad)
    
    dinomo=(('Vacio','Vacio'),( 'Solicitado pero pendiente de enviarmelo','Solicitado pero pendiente de enviarmelo'), ('Completado','Completado'), ('Investigar','Investigar'))
    dinomoDis=forms.ChoiceField( choices=dinomo)
    
    
