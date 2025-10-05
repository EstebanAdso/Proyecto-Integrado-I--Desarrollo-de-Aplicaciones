# Guía de Despliegue en Render

## Dependencias Agregadas

✅ **pandas==2.2.0** - Para procesamiento de datos CSV
✅ **gunicorn==21.2.0** - Servidor WSGI para producción
✅ **whitenoise==6.6.0** - Para servir archivos estáticos en producción

---

## Configuración en Render

### 1. Crear nuevo Web Service

1. Ve a https://render.com y crea una cuenta o inicia sesión
2. Haz clic en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub/GitLab

### 2. Configuración del Web Service

**Name:** `aplicacion-desercion` (o el nombre que prefieras)

**Environment:** `Python 3`

**Build Command:**
```bash
./build.sh
```

**Start Command:**
```bash
gunicorn aplicacion_desercion.wsgi:application
```

**Plan:** Free (o el que prefieras)

---

## 3. Variables de Entorno (Environment Variables)

En la sección "Environment" de Render, agrega las siguientes variables:

| Key | Value | Descripción |
|-----|-------|-------------|
| `SECRET_KEY` | `django-insecure-fr*4dg*b0b+yshs4)d5q&1xfb*y^-b=il1_v$ikgv+tp96843k` | Clave secreta (puedes usar esta o generar una nueva) |
| `DEBUG` | `False` | Desactivar modo debug en producción |
| `ALLOWED_HOSTS` | `proyecto-integrado-i-desarrollo-de.onrender.com` | **SIN** https:// |
| `DATABASE_URL` | `postgresql://desercion_db_bfxp_user:ijyZKBb0kjF6Ndq7AAcnAh4gnfmRvDBY@dpg-d3hagmogjchc73abv6n0-a/desercion_db_bfxp` | Base de datos PostgreSQL de Render (Internal URL) |

### Generar SECRET_KEY

Puedes generar una nueva SECRET_KEY ejecutando en Python:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

---

## 4. Base de Datos PostgreSQL

### Opción A: Usar PostgreSQL de Render (Recomendado)

1. En Render, crea un nuevo "PostgreSQL" database
2. Una vez creado, Render te dará las credenciales:
   - Internal Database URL
   - Hostname
   - Port
   - Database
   - Username
   - Password
3. Usa estos valores para las variables de entorno DB_*

### Opción B: Usar otra base de datos externa

Usa las credenciales de tu base de datos PostgreSQL existente.

---

## 5. Verificar el Despliegue

Una vez que Render complete el build y el deploy:

1. Accede a tu URL: `https://tu-app.onrender.com`
2. Verifica que la aplicación carga correctamente
3. Prueba el login y las funcionalidades principales

---

## Comandos Útiles

### Si necesitas ejecutar migraciones manualmente:
```bash
python manage.py migrate
```

### Si necesitas crear un superusuario:
```bash
python manage.py createsuperuser
```

### Ver logs en Render:
- Ve a tu servicio → pestaña "Logs"

---

## Troubleshooting

### Error: "DisallowedHost at /"
- Verifica que `ALLOWED_HOSTS` incluya tu dominio de Render

### Error: "No static files"
- Verifica que el comando `collectstatic` se ejecutó en build.sh
- Verifica que whitenoise esté en MIDDLEWARE

### Error de conexión a BD
- Verifica las variables de entorno DB_*
- Asegúrate de que la BD PostgreSQL está activa

---

## Notas Importantes

⚠️ **No uses la SECRET_KEY por defecto en producción**
⚠️ **Siempre usa DEBUG=False en producción**
⚠️ **Asegúrate de tener backups de tu base de datos**
