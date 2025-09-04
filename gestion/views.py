from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ColegioForm, SubirArchivoForm
from .models import Colegio, Estudiante, Asistencia
from django.db import transaction, models
from django.db.models.functions import TruncMonth
import pandas as pd
import io
from datetime import date, timedelta

# ---------- VISTAS ----------

# Vista para registrar un nuevo colegio
def crear_colegio(request):
    if request.method == "POST":
        form = ColegioForm(request.POST)
        if form.is_valid():
            nuevo_colegio = form.save()
            messages.success(request, "Institución educativa registrada exitosamente.")
            # Redirigimos a la página para subir archivos de este nuevo colegio
            return redirect("subir_archivo", id_colegio=nuevo_colegio.id_colegio)
    else:
        form = ColegioForm()
    return render(request, "gestion/crear_colegio.html", {"form": form})


# Vista para subir archivos
@transaction.atomic
def subir_archivo(request, id_colegio):
    colegio = get_object_or_404(Colegio, pk=id_colegio)
    if request.method == "POST":
        form = SubirArchivoForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_csv = request.FILES["archivo_csv"]

            if not archivo_csv.name.endswith('.csv'):
                messages.error(request, 'El archivo debe tener formato CSV.')
                return redirect("subir_archivo", id_colegio=colegio.id_colegio)

            try:
                # Decodificar y leer el archivo CSV con pandas
                data = io.StringIO(archivo_csv.read().decode('utf-8'))
                df = pd.read_csv(data)

                registros_creados = 0
                for _, row in df.iterrows():
                    # Usamos get_or_create para no duplicar estudiantes
                    estudiante, _ = Estudiante.objects.get_or_create(
                        nombre=row['nombre'],
                        apellidos=row['apellidos'],
                        fecha_nacimiento=row['fecha_nacimiento'],
                        colegio=colegio,  # Asociamos al colegio actual
                        defaults={'genero': row['genero'], 'grado': row['grado']}
                    )

                    # Convertimos el estado a un valor booleano
                    estado = True if str(row['estado_asistencia']).strip().lower() == 'presente' else False

                    # Usamos update_or_create para evitar duplicados de asistencia
                    Asistencia.objects.update_or_create(
                        estudiante=estudiante,
                        fecha=row['fecha_asistencia'],
                        defaults={'estado': estado}
                    )
                    registros_creados += 1
                messages.success(request, f"Archivo procesado. Se crearon o actualizaron {registros_creados} registros.")
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo: {e}")

            # Redirigimos al nuevo dashboard tras subir el archivo
            return redirect("dashboard_colegio", id_colegio=colegio.id_colegio)
    else:
        form = SubirArchivoForm()
    return render(request, "gestion/subir_archivo.html", {"form": form, "colegio": colegio})


def dashboard_colegio(request, id_colegio):
    colegio = get_object_or_404(Colegio, pk=id_colegio)
    estudiantes = Estudiante.objects.filter(colegio=colegio)

    # --- Inicia el Pipeline de Datos ---

    # 1. Distribución por Género
    genero_data = estudiantes.values('genero').annotate(count=models.Count('genero')).order_by('genero')
    genero_labels = [item['genero'] for item in genero_data]
    genero_values = [item['count'] for item in genero_data]

    # 2. Distribución por Grado
    grado_data = estudiantes.values('grado').annotate(count=models.Count('grado')).order_by('grado')
    grado_labels = [item['grado'] for item in grado_data]
    grado_values = [item['count'] for item in grado_data]

    # 3. Distribución por Edad
    edades = []
    today = date.today()
    for est in estudiantes:
        edad = today.year - est.fecha_nacimiento.year - ((today.month, today.day) < (est.fecha_nacimiento.month, est.fecha_nacimiento.day))
        edades.append(edad)

    # Agrupar edades en rangos (bins)
    bins = [0, 8, 11, 14, 18] # Rangos: 0-8, 9-11, 12-14, 15-18
    labels = ['0-8 años', '9-11 años', '12-14 años', '15-18 años']
    if edades:
        edad_series = pd.Series(edades)
        edad_counts = pd.cut(edad_series, bins=bins, labels=labels, right=False).value_counts().sort_index()
        edad_labels = edad_counts.index.tolist()
        edad_values = edad_counts.values.tolist()
    else:
        edad_labels = []
        edad_values = []

    # 4. Tendencia de Ausentismo (Deserción)
    today = date.today()

    # Obtenemos las ausencias del año y las agrupamos por mes
    ausencias_por_mes = Asistencia.objects.filter(
        estudiante__colegio=colegio,
        estado=False,
        fecha__year=today.year
    ).values('fecha').annotate(
        month=TruncMonth('fecha')
    ).values('month').annotate(
        total_ausencias=models.Count('id_asistencia')
    ).order_by('month')

    # Creamos un diccionario para búsqueda rápida
    ausencias_dict = {item['month'].month: item['total_ausencias'] for item in ausencias_por_mes}

    # Generamos las etiquetas y valores para los 12 meses del año
    meses_espanol = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    desercion_labels = meses_espanol
    desercion_values = [ausencias_dict.get(i, 0) for i in range(1, 13)]

    # --- Fin del Pipeline ---

    context = {
        'colegio': colegio,
        'total_estudiantes': estudiantes.count(),
        'chart_data': {
            'genero_labels': genero_labels,
            'genero_values': genero_values,
            'grado_labels': grado_labels,
            'grado_values': grado_values,
            'edad_labels': edad_labels,
            'edad_values': edad_values,
            'desercion_labels': desercion_labels,
            'desercion_values': desercion_values,
        }
    }
    return render(request, "gestion/dashboard_colegio.html", context)
