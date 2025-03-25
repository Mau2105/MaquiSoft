from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Trabajador, Maquina, Complemento, Operacion, Rol

class CustomUserCreationForm(UserCreationForm):
    nombre = forms.CharField(max_length=45, label="Nombre", required=True, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan'}))
    apellido = forms.CharField(max_length=45, label="Apellido", required=True, widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez'}))
    cedula = forms.IntegerField(label="Cédula", required=True, widget=forms.NumberInput(attrs={'placeholder': 'Ejemplo: 1075327167'}))
    telefono = forms.IntegerField(label="Teléfono", required=True, widget=forms.NumberInput(attrs={'placeholder': 'Ejemplo: 3026837124'}))
    username = forms.CharField(max_length=150, label="Usuario", required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario para iniciar sesión'}))
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Ejemplo: Contraseña123!'}))
    password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'placeholder': 'Confirme: Contraseña123!'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'nombre', 'apellido', 'cedula', 'telefono']

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if Trabajador.objects.filter(cedula=cedula).exists():
            raise forms.ValidationError("Esta cédula ya está registrada.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if Trabajador.objects.filter(telefono=telefono).exists():
            raise forms.ValidationError("Este teléfono ya está registrado.")
        return telefono

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class TrabajadorForm(forms.ModelForm):
    password = forms.CharField(
        label="Nueva contraseña (opcional)",
        widget=forms.PasswordInput(attrs={'placeholder': 'Dejar en blanco para no cambiar'}),
        required=False
    )

    class Meta:
        model = Trabajador
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'rol', 'pin']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Juan'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Ejemplo: Pérez'}),
            'cedula': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 1075327167'}),
            'telefono': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 3026837124'}),
            'pin': forms.NumberInput(attrs={'placeholder': 'PIN opcional'}),
        }

    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if self.instance and self.instance.pk:
            if Trabajador.objects.filter(cedula=cedula).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Esta cédula ya está registrada.")
        else:
            if Trabajador.objects.filter(cedula=cedula).exists():
                raise forms.ValidationError("Esta cédula ya está registrada.")
        return cedula

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if self.instance and self.instance.pk:
            if Trabajador.objects.filter(telefono=telefono).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError("Este teléfono ya está registrado.")
        else:
            if Trabajador.objects.filter(telefono=telefono).exists():
                raise forms.ValidationError("Este teléfono ya está registrado.")
        return telefono

class MaquinaForm(forms.ModelForm):
    DISPONIBILIDAD_CHOICES = [
        ('SÍ', 'Sí'),
        ('NO', 'No'),
    ]
    ESTADO_MAQUINA_CHOICES = [
        ('Disponible', 'Disponible'),
        ('En uso', 'En uso'),
        ('En mantenimiento', 'En mantenimiento'),
        ('Fuera de servicio', 'Fuera de servicio'),
    ]
    
    disponibilidad = forms.ChoiceField(
        choices=DISPONIBILIDAD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Disponibilidad",
        required=True
    )
    estado_maquina = forms.ChoiceField(
        choices=ESTADO_MAQUINA_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Estado de la Máquina",
        required=True
    )

    class Meta:
        model = Maquina
        fields = '__all__'
        widgets = {
            'marca': forms.TextInput(attrs={'placeholder': 'Ejemplo: Caterpillar'}),
            'tipo': forms.TextInput(attrs={'placeholder': 'Ejemplo: Excavadora'}),
            'cilindraje': forms.TextInput(attrs={'placeholder': 'Ejemplo: 2000 cc'}),
            'modelo': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 2023'}),
            'serial': forms.TextInput(attrs={'placeholder': 'Ejemplo: CAT12345'}),
            'kilometraje': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 15000'}),
            'tipo_combustible': forms.TextInput(attrs={'placeholder': 'Ejemplo: Diésel'}),
        }

class ComplementoForm(forms.ModelForm):
    class Meta:
        model = Complemento
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ejemplo: Martillo'}),
            'tipo': forms.NumberInput(attrs={'placeholder': 'Ejemplo: 1'}),
            'estado': forms.TextInput(attrs={'placeholder': 'Ejemplo: Operativo'}),
        }

class OperacionForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = '__all__'
        widgets = {
            'fecha_entrada': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_salida': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'area': forms.TextInput(attrs={'placeholder': 'Ejemplo: Zona 1'}),
            'consumo': forms.TextInput(attrs={'placeholder': 'Ejemplo: 10 litros'}),
            'observaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Notas adicionales'}),
            'tiempo_operacion': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'tipo_operacion': forms.TextInput(attrs={'placeholder': 'Ejemplo: Excavación'}),
        }