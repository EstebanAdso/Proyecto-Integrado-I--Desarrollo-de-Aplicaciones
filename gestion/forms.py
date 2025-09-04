from django import forms
from .models import Colegio

class ColegioForm(forms.ModelForm):
    """Formulario para crear una nueva institución educativa."""
    class Meta:
        model = Colegio
        fields = [
            "nombre",
            "codigo_dane",
            "ubicacion",
        ]
        labels = {
            "nombre": "Nombre de la institución educativa",
        }

class SubirArchivoForm(forms.Form):
    archivo_csv = forms.FileField(label="Selecciona un archivo CSV")
