# 🎨 Galería de Arte - Proyecto Escolar

Este proyecto es una **aplicación web distribuida** compuesta por una **API RESTful** en Python (FastAPI) y un cliente HTML/JS. La plataforma permite que dos tipos de usuarios (Artistas y Observadores) interactúen mediante obras, subastas y ofertas.

---

## 🧱 Estructura general

- `art-gallery-api/`: Backend con FastAPI (API REST)
- `art-gallery-client/`: Interfaz HTML estática

---

## ⚙️ Requisitos para ejecutar el backend

- Python 3.10 o superior
- pip (administrador de paquetes)
- Entorno virtual (recomendado)

---

## 📦 Instalación del backend

1. Clonar el repositorio:
```bash
git clone https://github.com/FernandLvl/art-gallery-api.git
cd art-gallery-api
```

2. Crear y activar un entorno virtual:
```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

4. Crear la base de datos SQLite:
```bash
python db_init.py
```

5. Ejecutar el servidor:
```bash
uvicorn app.main:app --reload
```

6. Abrir la API en el navegador:
```arduino
http://127.0.0.1:8000/docs
```

## 📁 Archivos importantes

`main.py`: Entrada principal del backend

`app/services/`: Endpoints REST organizados

`app/business/`: Lógica de negocio

`app/data/`: Base de datos y modelos

`static/uploads/`: Carpeta para imágenes subidas

## 👥 Roles y funcionalidades
### Artista:
- Registro e inicio de sesión

- Subir obras de arte

- Iniciar subastas

- Ver sus obras y subastas

### Observador:
- Navegar por obras y subastas activas

- Ver detalles de subastas

- Hacer ofertas en subastas

- Ver historial de sus ofertas

## 🔐 Seguridad
- Autenticación con JWT

- Cifrado de contraseñas con bcrypt

- Acceso basado en roles

- Protección de endpoints sensibles
