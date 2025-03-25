# act1/models.py
from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    nombre = models.CharField(max_length=45, unique=True)  # Ejemplo: "Administrador", "Operador"
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional del rol

    def __str__(self):
        return self.nombre

class Complemento(models.Model):
    nombre = models.CharField(max_length=45)
    tipo = models.IntegerField()  # Podrías usar choices para tipos específicos si aplica
    estado = models.CharField(max_length=45)  # Ejemplo: "Operativo", "En mantenimiento"

    def __str__(self):
        return self.nombre

class Maquina(models.Model):
    ESTADO_MAQUINA_CHOICES = [
        ('Disponible', 'Disponible'),
        ('En uso', 'En uso'),
        ('En mantenimiento', 'En mantenimiento'),
        ('Fuera de servicio', 'Fuera de servicio'),
    ]
    DISPONIBILIDAD_CHOICES = [
        ('SÍ', 'Sí'),
        ('NO', 'No'),
    ]
    
    marca = models.CharField(max_length=45)
    tipo = models.CharField(max_length=45)
    estado_maquina = models.CharField(max_length=45, choices=ESTADO_MAQUINA_CHOICES, default='Disponible')
    cilindraje = models.CharField(max_length=45)
    modelo = models.IntegerField()
    serial = models.CharField(max_length=45)
    disponibilidad = models.CharField(max_length=2, choices=DISPONIBILIDAD_CHOICES, default='SÍ')
    kilometraje = models.IntegerField()
    tipo_combustible = models.CharField(max_length=45)  # Ejemplo: "Gasolina", "Diésel"
    complemento = models.ForeignKey(Complemento, on_delete=models.CASCADE)

    def __str__(self):
        return self.marca

class Trabajador(models.Model):
    nombre = models.CharField(max_length=45)
    apellido = models.CharField(max_length=45)
    cedula = models.IntegerField(unique=True)  # Añadido unique para evitar duplicados
    telefono = models.BigIntegerField(unique=True)  # Añadido unique para evitar duplicados
    pin = models.IntegerField(null=True, blank=True)  # Permitimos que sea NULL
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Operacion(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField()
    area = models.CharField(max_length=100)
    consumo = models.CharField(max_length=45)  # Ejemplo: "10 litros"
    observaciones = models.TextField()
    tiempo_operacion = models.FloatField(null=True, blank=True, verbose_name="Tiempo de Operación (horas)")
    tipo_operacion = models.CharField(max_length=45)  # Ejemplo: "Excavación", "Transporte"

    def __str__(self):
        return f"Operación {self.id}"