from django.shortcuts import render, get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import modelformset_factory
from .models import Receta, categoria, RecetaIngrediente, Valoracion
from .forms import RecetaForm, RecetaIngredienteForm, ValoracionForm

# Autetificación

def registro(request):
    if request.user.is_authenticated:
        return redirect('listado_recetas')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}!")
            return redirect('listado_recetas')
        else:
            form = UserCreationForm()
        return render(request, 'registro.html', {'form': form})
    
def login_view(request):
    if request.user.is_authenticated:
        return redirect('listado_recetas')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"¡Bienvenido de nuevo, {user.username}!")
            return redirect(request.GET.get("next", "listado_recetas"))
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "¡Has cerrado sesión exitosamente!")
    return redirect('listado_recetas')

# Lista de Recetas

def listado_recetas(request):
    recetas = Receta.objects.filter(publicado=True).select_related("autor", "categoria")
    categorias = categoria.objects.all()
 
    categoria_slug = request.GET.get("categoria")
    categoria_activa = None
    if categoria_slug:
        categoria_activa = get_object_or_404(categoria, slug=categoria_slug)
        recetas = recetas.filter(categoria=categoria_activa)
 
    query = request.GET.get("q", "").strip()
    if query:
        recetas = recetas.filter(titulo__icontains=query)
 
    orden = request.GET.get("orden", "-creado_en")
    opciones_orden = {
        "-creado_en": "-creado_en",
        "titulo": "titulo",
        "tiempo_preparacion": "tiempo_preparacion",
    }
    recetas = recetas.order_by(opciones_orden.get(orden, "-creado_en"))
 
    return render(request, "recetas/listado.html", {
        "recetas": recetas,
        "categorias": categorias,
        "categoria_activa": categoria_activa,
        "query": query,
        "orden": orden,
    })

# Detalle de Receta

def detalle_receta(request, slug):
    receta = get_object_or_404(Receta, slug=slug, publicado=True)
    ingredientes = receta.receta_ingredientes.select_related("ingrediente")
    valoraciones = receta.valoraciones.select_related("autor")
    ya_valoro = (
        request.user.is_authenticated and
        valoraciones.filter(autor=request.user).exists()
    )
    form_valoracion = ValoracionForm() if request.user.is_authenticated and not ya_valoro else None
 
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(request, "Debes iniciar sesión para comentar.")
            return redirect("login")
        if ya_valoro:
            messages.error(request, "Ya has valorado esta receta.")
            return redirect("detalle_receta", slug=slug)
 
        form_valoracion = ValoracionForm(request.POST)
        if form_valoracion.is_valid():
            valoracion = form_valoracion.save(commit=False)
            valoracion.receta = receta
            valoracion.autor = request.user
            valoracion.save()
            messages.success(request, "¡Valoración enviada!")
            return redirect("detalle_receta", slug=slug)
 
    return render(request, "recetas/detalle.html", {
        "receta": receta,
        "ingredientes": ingredientes,
        "valoraciones": valoraciones,
        "form_valoracion": form_valoracion,
        "ya_valoro": ya_valoro,
    })

# Eliminar valoración


@login_required
def eliminar_valoracion(request, pk):
    valoracion = get_object_or_404(Valoracion, pk=pk, autor=request.user)
    slug = valoracion.receta.slug
    if request.method == "POST":
        valoracion.delete()
        messages.success(request, "Comentario eliminado.")
    return redirect("detalle_receta", slug=slug)

# Crear Receta

@login_required
def crear_receta(request):
    IngredienteFormSet = modelformset_factory(
        RecetaIngrediente,
        form=RecetaIngredienteForm,
        extra=3,
        can_delete=True,
    )
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        formset = IngredienteFormSet(request.POST, queryset=RecetaIngrediente.objects.none())
        if form.is_valid() and formset.is_valid():
            receta = form.save(commit=False)
            receta.autor = request.user
            receta.save()
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get("DELETE"):
                    ing = f.save(commit=False)
                    ing.receta = receta
                    ing.save()
            messages.success(request, "¡Receta creada correctamente!")
            return redirect("detalle_receta", slug=receta.slug)
    else:
        form = RecetaForm()
        formset = IngredienteFormSet(queryset=RecetaIngrediente.objects.none())
 
    return render(request, "recetas/form_receta.html", {
        "form": form,
        "formset": formset,
        "accion": "Crear",
    })

# Editar Receta

@login_required
def editar_receta(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    if receta.autor != request.user:
        messages.error(request, "No tienes permiso para editar esta receta.")
        return redirect("detalle_receta", slug=slug)
 
    IngredienteFormSet = modelformset_factory(
        RecetaIngrediente,
        form=RecetaIngredienteForm,
        extra=1,
        can_delete=True,
    )
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        formset = IngredienteFormSet(
            request.POST,
            queryset=RecetaIngrediente.objects.filter(receta=receta)
        )
        if form.is_valid() and formset.is_valid():
            form.save()
            for f in formset:
                if f.cleaned_data:
                    if f.cleaned_data.get("DELETE"):
                        if f.instance.pk:
                            f.instance.delete()
                    else:
                        ing = f.save(commit=False)
                        ing.receta = receta
                        ing.save()
            messages.success(request, "¡Receta actualizada correctamente!")
            return redirect("detalle_receta", slug=receta.slug)
    else:
        form = RecetaForm(instance=receta)
        formset = IngredienteFormSet(
            queryset=RecetaIngrediente.objects.filter(receta=receta)
        )
 
    return render(request, "recetas/form_receta.html", {
        "form": form,
        "formset": formset,
        "receta": receta,
        "accion": "Editar",
    })


# Eliminar Receta

@login_required
def eliminar_receta(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    if receta.autor != request.user:
        messages.error(request, "No tienes permiso para eliminar esta receta.")
        return redirect("detalle_receta", slug=slug)
    if request.method == "POST":
        receta.delete()
        messages.success(request, "Receta eliminada.")
        return redirect("listado_recetas")
    return render(request, "recetas/confirmar_eliminar.html", {"receta": receta})


# Perfil de Usuario

def perfil_usuario(request, username):
    from django.contrib.auth.models import User
    usuario = get_object_or_404(User, username=username)
    recetas = Receta.objects.filter(autor=usuario, publicado=True).order_by("-creado_en")
    return render(request, "recetas/perfil.html", {
        "usuario": usuario,
        "recetas": recetas,
    })
