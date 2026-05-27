"""
URL configuration for config project.

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
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Rutas de registro
    path("registro/", views.registro, name="registro"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Rutas de recetas
    path("", views.listado_recetas, name="listado_recetas"),
    path("reta/nueva/", views.crear_receta, name="crear_receta"),
    path("receta/<slug:slug>/", views.detalle_receta, name="detalle_receta"),
    path("receta/<slug:slug>/editar/", views.editar_receta, name="editar_receta"),
    path("receta/<slug:slug>/eliminar/", views.eliminar_receta, name="eliminar_receta"),

    # Ruta de perfil de usuario
    path("perfil/<str:username>/", views.perfil_usuario, name="perfil_usuario"),

    #valoraciones
    path("receta/<slug:slug>/valorar/", views.valorar_receta, name="valorar_receta"),   
    
]
