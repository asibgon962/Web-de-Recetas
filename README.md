# 🍳 La Cocina de Casa

Plataforma web de recetas caseras desarrollada con Django. Permite a los usuarios publicar, descubrir y guardar recetas con un diseño cálido y rústico.

---

## 📋 Descripción

**La Cocina de Casa** es una aplicación web completa donde los usuarios pueden registrarse, publicar sus propias recetas con ingredientes detallados e instrucciones paso a paso, valorar y comentar las recetas de otros usuarios, y guardar sus favoritas en su perfil personal.

---

## ✨ Funcionalidades

### Recetas
- Listado de recetas con búsqueda por texto y filtro por categoría
- Ordenación por fecha, nombre o tiempo de preparación
- Página de detalle con imagen, ingredientes, instrucciones y metadatos (tiempo, porciones, dificultad)
- Crear, editar y eliminar recetas (solo el autor)
- Subida de imagen por receta
- Sistema de ingredientes detallado (cantidad + unidad + nota)

### Usuarios
- Registro y login propio
- Perfil personalizado con foto y biografía
- Página de perfil con recetas publicadas y favoritos
- Solo usuarios autenticados pueden crear, editar o eliminar recetas
- Solo el autor puede modificar sus propias recetas

### Valoraciones
- Sistema de puntuación de 1 a 5 estrellas
- Comentarios por receta
- Un usuario solo puede valorar cada receta una vez
- El autor puede eliminar sus propios comentarios

### Favoritos
- Guardar y quitar recetas de favoritos
- Sección de favoritos en el perfil personal

---

## 🛠️ Tecnologías usadas

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.11 | Lenguaje principal |
| Django | 5.2 | Framework web |
| SQLite | — | Base de datos |
| Bootstrap | 5.3 | Framework CSS |
| Bootstrap Icons | 1.11 | Iconografía |
| Google Fonts | — | Tipografías (Playfair Display, Lato) |
| Pillow | — | Procesamiento de imágenes |

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/asibgon962/Web-de-Recetas.git
cd Web-de-Recetas
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias

```bash
pip install django pillow
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear un superusuario (opcional, para acceder al admin)

```bash
python manage.py createsuperuser
```

### 6. Arrancar el servidor

```bash
python manage.py runserver
```

Abre el navegador en **http://127.0.0.1:8000**

> El panel de administración está disponible en **http://127.0.0.1:8000/admin**

---

## 📁 Estructura del proyecto

```
Web-de-Recetas/
│
├── config/                  # Configuración del proyecto Django
│   ├── settings.py          # Ajustes generales
│   ├── urls.py              # URLs principales
│   ├── wsgi.py
│   └── asgi.py
│
├── recetas/                 # App principal
│   ├── migrations/          # Migraciones de base de datos
│   ├── models.py            # Modelos: Receta, Ingrediente, Categoría, Valoracion, PerfilUsuario
│   ├── views.py             # Vistas
│   ├── urls.py              # URLs de la app
│   ├── forms.py             # Formularios
│   └── admin.py             # Registro en el panel de administración
│
├── templates/               # Templates HTML
│   ├── base.html            # Template base con navbar y footer
│   ├── listado.html         # Listado de recetas con búsqueda y filtros
│   ├── detalle.html         # Detalle de receta + comentarios
│   ├── form_receta.html     # Formulario crear/editar receta
│   ├── perfil.html          # Perfil de usuario
│   ├── editar_perfil.html   # Editar perfil
│   ├── login.html           # Inicio de sesión
│   ├── registro.html        # Registro de usuario
│   └── confirmar_eliminar.html
│
├── media/                   # Archivos subidos por usuarios (imágenes)
├── static/                  # Archivos estáticos
├── db.sqlite3               # Base de datos
└── manage.py
```

---

## 👤 Autor

**Álvaro Sibón** — [@asibgon962](https://github.com/asibgon962)