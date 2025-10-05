#!/usr/bin/env bash
# Script de build para Render

set -o errexit  # Salir si hay errores

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Recolectar archivos estáticos
python manage.py collectstatic --no-input

# Ejecutar migraciones
python manage.py migrate
