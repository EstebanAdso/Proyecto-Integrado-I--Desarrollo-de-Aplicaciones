from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import Colegio, Usuario

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


class RegistroUsuarioForm(UserCreationForm):
    """Formulario personalizado para registro de usuarios."""
    first_name = forms.CharField(
        max_length=150, 
        required=True,
        label="Nombres",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tus nombres'
        })
    )
    last_name = forms.CharField(
        max_length=150, 
        required=True,
        label="Apellidos",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tus apellidos'
        })
    )
    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'correo@ejemplo.com'
        })
    )
    institucion_educativa = forms.CharField(
        max_length=255,
        required=True,
        label="Institución educativa",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de tu institución educativa'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=False,
        label="Nombre de usuario (opcional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de usuario (opcional)'
        }),
        help_text="Si no se especifica, se generará automáticamente basado en tu email."
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'institucion_educativa', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplicar clases Bootstrap a todos los campos
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirma tu contraseña'
        })
        
        # Personalizar etiquetas
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar contraseña"

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.institucion_educativa = self.cleaned_data['institucion_educativa']
        
        # Si se proporciona username, usarlo; si no, se generará automáticamente en el modelo
        if self.cleaned_data.get('username'):
            user.username = self.cleaned_data['username']
            
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Formulario personalizado para login que acepta email o username."""
    username = forms.CharField(
        label="Correo electrónico o usuario",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico o nombre de usuario',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Tu contraseña'
        })
    )

    def clean(self):
        username_or_email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            # Primero intentar con el valor tal como está (por si es username)
            self.user_cache = authenticate(
                self.request, 
                username=username_or_email, 
                password=password
            )
            
            # Si no funciona, intentar buscando por email
            if self.user_cache is None:
                try:
                    user_by_email = Usuario.objects.get(email=username_or_email)
                    self.user_cache = authenticate(
                        self.request,
                        username=user_by_email.username,
                        password=password
                    )
                except Usuario.DoesNotExist:
                    pass
            
            if self.user_cache is None:
                raise forms.ValidationError(
                    "Correo electrónico/usuario o contraseña incorrectos.",
                    code='invalid_login'
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data
