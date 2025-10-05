# 🚀 GUÍA RÁPIDA DE DESPLIEGUE EN RENDER

## ✅ CHECKLIST PRE-DESPLIEGUE

- [x] requirements.txt completo con todas las dependencias
- [x] build.sh configurado
- [x] settings.py listo para producción
- [x] Base de datos PostgreSQL en Render creada
- [x] .gitignore incluye .env y staticfiles/
- [x] Migraciones aplicadas localmente

---

## 📦 PASO 1: SUBIR CÓDIGO A GITHUB

```bash
# Inicializar repositorio (si no está inicializado)
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar proyecto para despliegue en Render"

# Conectar con GitHub (reemplaza con tu URL)
git remote add origin https://github.com/TU-USUARIO/TU-REPOSITORIO.git

# Subir a GitHub
git push -u origin main
```

**⚠️ IMPORTANTE:** Verifica que `.env` NO se haya subido a GitHub. El archivo debe estar en rojo/ignorado.

---

## 🌐 PASO 2: CREAR WEB SERVICE EN RENDER

1. Ve a https://render.com/dashboard
2. Click en **"New +"** → **"Web Service"**
3. **Connect Repository:** Selecciona tu repositorio de GitHub
4. **Configuración:**

### **Información Básica**
- **Name:** `aplicacion-desercion` (o el nombre que prefieras)
- **Region:** Oregon (USA West)
- **Branch:** `main`
- **Root Directory:** (dejar vacío)
- **Environment:** `Python 3`

### **Build & Deploy**
- **Build Command:**
  ```bash
  ./build.sh
  ```

- **Start Command:**
  ```bash
  gunicorn aplicacion_desercion.wsgi:application
  ```

### **Plan**
- Selecciona: **Free** (o el plan que prefieras)

---

## 🔐 PASO 3: CONFIGURAR VARIABLES DE ENTORNO

En la sección **"Environment"** del Web Service, agrega estas variables:

### Variables Requeridas:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Genera una nueva clave (ver abajo) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `aplicacion-desercion.onrender.com` |
| `DATABASE_URL` | `postgresql://desercion_db_bfxp_user:ijyZKBb0kjF6Ndq7AAcnAh4gnfmRvDBY@dpg-d3hagmogjchc73abv6n0-a/desercion_db_bfxp` |

**⚠️ IMPORTANTE sobre DATABASE_URL:**
- Usa la **Internal Database URL** (sin `.oregon-postgres.render.com`)
- Esta es más rápida porque la conexión es interna dentro de Render

### Generar SECRET_KEY

Ejecuta esto en tu terminal local:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo como `SECRET_KEY`.

### Actualizar ALLOWED_HOSTS

Una vez que tu app esté desplegada, Render te dará una URL como:
- `https://aplicacion-desercion.onrender.com`

Actualiza `ALLOWED_HOSTS` con esa URL exacta (sin https://).

---

## 🎯 PASO 4: DESPLEGAR

1. Click en **"Create Web Service"**
2. Render comenzará el proceso de build automáticamente
3. Podrás ver los logs en tiempo real

### Logs que verás:

```
==> Cloning from https://github.com/...
==> Running build command './build.sh'...
==> Installing dependencies...
==> Collecting static files...
==> Running migrations...
==> Build successful!
==> Starting service with 'gunicorn aplicacion_desercion.wsgi:application'...
==> Your service is live at https://...onrender.com
```

**⏱️ Tiempo estimado:** 3-5 minutos para el primer despliegue.

---

## ✅ PASO 5: VERIFICAR EL DESPLIEGUE

1. **Acceder a la aplicación:**
   - Ve a la URL que te dio Render
   - Ejemplo: `https://aplicacion-desercion.onrender.com`

2. **Verificar funcionalidades:**
   - ✅ Página principal carga correctamente
   - ✅ Login funciona
   - ✅ Registro de usuarios funciona
   - ✅ Dashboard muestra datos

3. **Crear superusuario (si es necesario):**
   - En Render, ve a tu Web Service
   - Click en **"Shell"** (en el menú lateral)
   - Ejecuta:
     ```bash
     python manage.py createsuperuser
     ```
   - Accede al admin: `https://tu-app.onrender.com/admin/`

---

## 🔧 COMANDOS ÚTILES EN RENDER SHELL

### Ver estado de migraciones:
```bash
python manage.py showmigrations
```

### Aplicar migraciones pendientes:
```bash
python manage.py migrate
```

### Crear datos de prueba:
```bash
python manage.py shell
```

### Ver logs en tiempo real:
Ve a tu servicio → Pestaña **"Logs"**

---

## 🐛 TROUBLESHOOTING

### Error: "DisallowedHost at /"
**Solución:** Actualiza `ALLOWED_HOSTS` en las variables de entorno con tu URL de Render.

### Error: "No module named 'X'"
**Solución:** Verifica que la dependencia esté en `requirements.txt` y vuelve a desplegar.

### Error: "relation does not exist"
**Solución:** Las migraciones no se aplicaron. En Render Shell ejecuta:
```bash
python manage.py migrate
```

### Error: "Static files not found"
**Solución:** Verifica que `build.sh` ejecute `collectstatic` correctamente.

### La app tarda en cargar
**Nota:** En el plan gratuito, la app se "duerme" después de 15 minutos de inactividad. La primera carga puede tardar 30-60 segundos.

---

## 📊 MONITOREO

### Ver logs en tiempo real:
```bash
# Desde el dashboard de Render
Web Service → Logs
```

### Métricas:
```bash
# Render muestra automáticamente:
- CPU usage
- Memory usage
- Request count
- Response time
```

---

## 🔄 ACTUALIZAR LA APLICACIÓN

Cada vez que hagas cambios en tu código:

```bash
# Hacer cambios en tu código local
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

**Render detectará automáticamente los cambios y redesplegar á la aplicación.**

---

## 📝 RESUMEN DE CONFIGURACIÓN

### Build Command:
```bash
./build.sh
```

### Start Command:
```bash
gunicorn aplicacion_desercion.wsgi:application
```

### Variables de Entorno Críticas:
- `SECRET_KEY` - Nueva clave secreta
- `DEBUG` - `False`
- `ALLOWED_HOSTS` - Tu URL de Render
- `DATABASE_URL` - Internal URL de PostgreSQL

---

## ✅ PROYECTO LISTO PARA PRODUCCIÓN

Tu aplicación Django está completamente configurada para producción con:
- ✅ Servidor WSGI (Gunicorn)
- ✅ Archivos estáticos (Whitenoise)
- ✅ Base de datos PostgreSQL
- ✅ Migraciones automáticas
- ✅ Variables de entorno seguras
- ✅ Procesamiento de CSV (Pandas)

**¡Tu aplicación está lista para desplegarse! 🎉**
