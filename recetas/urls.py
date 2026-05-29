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
    path("receta/nueva/", views.crear_receta, name="crear_receta"),
    path("receta/<slug:slug>/", views.detalle_receta, name="detalle_receta"),
    path("receta/<slug:slug>/editar/", views.editar_receta, name="editar_receta"),
    path("receta/<slug:slug>/eliminar/", views.eliminar_receta, name="eliminar_receta"),
    path("valoracion/<int:pk>/eliminar/", views.eliminar_valoracion, name="eliminar_valoracion"),
    # Ruta de perfil de usuario
    path("perfil/<str:username>/", views.perfil_usuario, name="perfil_usuario"),


]
