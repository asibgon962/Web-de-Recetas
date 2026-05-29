from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categorias"
        verbose_name = "categoria"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    

class Ingrediente(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "ingredientes"
        verbose_name = "ingrediente"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
class Receta(models.Model):
    DIFICULTAD_CHOICES = [
        ('facil', 'Facil'),
        ('media', 'Media'),
        ('dificil', 'Dificil'),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    descripcion = models.TextField()
    instrucciones = models.TextField()
    imagen = models.ImageField(upload_to='recetas/', blank=True, null=True)
    tiempo_preparacion = models.PositiveIntegerField(help_text="Tiempo de preparación en minutos")
    tiempo_coccion = models.PositiveIntegerField(help_text="Tiempo de cocción en minutos")
    porciones = models.PositiveIntegerField(default=4)
    dificultad = models.CharField(max_length=10, choices=DIFICULTAD_CHOICES, default='media')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recetas')
    categoria = models.ForeignKey(categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='recetas')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "recetas"
        verbose_name = "receta"
        ordering = ['-creado_en']
    
    def __str__(self):
        return self.titulo
    
    @property
    def tiempo_total(self):
        return self.tiempo_preparacion + self.tiempo_coccion
    
    @property
    def valoracion_media(self):
        valoraciones = self.valoraciones.all()
        if valoraciones.exists():
            return round(sum(v.valoracion for v in valoraciones) / valoraciones.count(), 1)
        return None
    
class RecetaIngrediente(models.Model):
    UNIDAD_CHOICES = [
        ("g", "Gramos"),
        ("kg", "Kilogramos"),
        ("ml", "Mililitros"),
        ("l", "Litros"),
        ("tsp", "Cucharadita"),
        ("tbsp", "Cucharada"),
        ("taza", "Taza"),
        ("unidad", "Unidad"),
        ("al_gusto", "Al gusto"),
    ]

    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='receta_ingredientes')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE, related_name="usos")
    cantidad = models.DecimalField( max_digits=7, decimal_places=2, null=True, blank=True)
    unidad = models.CharField(max_length=20, choices=UNIDAD_CHOICES, default='unidad')
    nota = models.CharField(max_length=200, blank=True, help_text="Ej: picado fino, a temperatura ambiente")

    class Meta:
        verbose_name= "Ingrediente de receta"
        verbose_name_plural = "Ingredientes de receta"
        unique_together = ('receta', 'ingrediente')

    def __str__(self):
        cantidad_str = f"{self.cantidad} {self.get_unidad_display()}" if self.cantidad else "Cantidad al gusto"
        return f"{cantidad_str} de {self.ingrediente.nombre} para {self.receta.titulo}"
    
class Valoracion(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='valoraciones')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='valoraciones')
    puntuacion = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "valoraciones"
        verbose_name = "valoracion"
        unique_together = ('receta', 'autor')
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.autor.username} valoró {self.receta.titulo} con {self.puntuacion} estrellas"
    
    