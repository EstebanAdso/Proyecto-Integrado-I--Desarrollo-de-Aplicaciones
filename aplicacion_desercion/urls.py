"""
URL configuration for aplicacion_desercion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestion.views import CustomLoginView, registro_usuario, logout_usuario

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de autenticación
    path('', CustomLoginView.as_view(), name='login'),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/registro/', registro_usuario, name='registro'),
    path('auth/logout/', logout_usuario, name='logout'),
    
    # URLs de la aplicación
    path('gestion/', include('gestion.urls')),   
]



