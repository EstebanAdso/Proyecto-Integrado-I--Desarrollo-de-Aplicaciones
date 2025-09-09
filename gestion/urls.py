# Incluye las URLs de la app gestion
from django.urls import path
from . import views   # Importamos las vistas de la app

urlpatterns = [
    # Dashboard principal
    path('dashboard/', views.dashboard_principal, name='dashboard_principal'),
    
    # Gestión de colegios
    path('crear-colegio/', views.crear_colegio, name='crear_colegio'),
    path('colegio/<int:id_colegio>/subir-archivo/', views.subir_archivo, name='subir_archivo'),
    path('colegio/<int:id_colegio>/dashboard/', views.dashboard_colegio, name='dashboard_colegio'),
]
