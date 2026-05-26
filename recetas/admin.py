from django.contrib import admin
from .models import categoria, Ingrediente, Receta, RecetaIngrediente, Valoracion

class RecetaIngredienteInline(admin.TabularInline):
    model = RecetaIngrediente
    extra = 3


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', "dificultad", 'publicado', 'creado_en')
    list_filter = ("dificultad", "publicado", "categoria")
    search_fields = ('titulo', 'descripcion')
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [RecetaIngredienteInline]


@admin.register(categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nombre',)}

@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):
    search_fields = ('nombre',)

@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    class ValoracionAdmin(admin.ModelAdmin):
        list_display = ('receta', 'usuario', 'puntuacion', 'comentario', 'creado_en')
        list_filter = ('puntuacion', 'creado_en')

