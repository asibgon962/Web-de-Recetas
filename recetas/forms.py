from django import forms
from django.utils.text import slugify
from .models import Receta, RecetaIngrediente, Valoracion


class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = [
            "titulo", "descripcion", "instrucciones",
            "imagen", "tiempo_preparacion", "tiempo_coccion",
            "porciones", "dificultad", "categoria", "publicado",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nombre de la receta"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "instrucciones": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "imagen": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "tiempo_preparacion": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "tiempo_coccion": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "porciones": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "dificultad": forms.Select(attrs={"class": "form-select"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "publicado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def save(self, commit=True):
        receta = super().save(commit=False)
        if not receta.slug:
            receta.slug = slugify(receta.titulo)
        if commit:
            receta.save()
        return receta


class RecetaIngredienteForm(forms.ModelForm):
    class Meta:
        model = RecetaIngrediente
        fields = ["ingrediente", "cantidad", "unidad", "nota"]
        widgets = {
            "ingrediente": forms.Select(attrs={"class": "form-select"}),
            "cantidad": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "unidad": forms.Select(attrs={"class": "form-select"}),
            "nota": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: picado fino"}),
        }


class ValoracionForm(forms.ModelForm):
    class Meta:
        model = Valoracion
        fields = ["valoracion", "comentario"]
        widgets = {
            "valoracion": forms.Select(
                choices=[(i, f"{i} ★") for i in range(1, 6)],
                attrs={"class": "form-select"}
            ),
            "comentario": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Cuéntanos qué te pareció..."}),
        }

