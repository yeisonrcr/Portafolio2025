"""
vehicle
"""
from django.contrib import admin
from django.urls import path
from gyna import views
from django.contrib.auth.views import LoginView,LogoutView




urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home_view,name=''),

    path('adminclick', views.adminclick_view),
    path('adminlogin', LoginView.as_view(template_name='vehicle/adminlogin.html'),name='adminlogin'),



    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    
    
    
    path('admin-request', views.admin_request_view,name='admin-request'),
    
    
    
    
    path('admin-view-request',views.admin_view_request_view,name='admin-view-request'),
    
    
    path('admin-view-request-clientepen',views.admin_pendientes_clientes,name='admin-view-request-clientepen'),
    
    
    path('admin-view-request-dineropen',views.admin_pendientes_dinero,name='admin-view-request-dineropen'),
    
    
    path('admin-view-request-distripen',views.admin_pendientes_distribuidoras,name='admin-view-request-distripen'),
    
    
    
    
    path('admin-view-request-investigar',views.admin_pendientes_investigar,name='admin-view-request-investigar'),
    
    path('admin-view-request-usa',views.admin_pendientes_usa,name='admin-view-request-usa'),
    
    path('admin-view-request-internet',views.admin_pendientes_internet,name='admin-view-request-internet'),
    
    path('admin-view-request-panama',views.admin_pendientes_panama,name='admin-view-request-panama'),
    
    path('admin-view-request-otros',views.admin_pendientes_otros,name='admin-view-request-otros'),
    
    
    
    
    
    path('admin-view-request-dispagados',views.admin_pendientes_distribuidoras_pagados,name='admin-view-request-dispagados'),
    
    
    path('change-status-uno/<int:pk>', views.change_status_view_uno,name='change-status'),
    
    
    
    path('change-status-dos/<int:pk>', views.change_status_view_dos,name='change-status-dos'),
    
    
    
    path('change-status-tres/<int:pk>', views.change_status_view_tres,name='change-status-tres'),
    
    
    path('admin-add-request',views.admin_add_request_view,name='admin-add-request'),
    
    path('admin-busqueda', views.admin_busqueda,name='admin-busqueda'),

    path('admin-cliente-busqueda', views.admin_cliente_busqueda,name='admin-cliente-busqueda'),
    
    path('admin-customer', views.admin_customer_view,name='admin-customer'),
    
    path('afterlogin', views.afterlogin_view,name='afterlogin'),



    
    #path('descargar-archivo', views.descargar_archivo,name='descargar-archivo'),



]


handler404 = "vehicle.views.error_404"
