from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Paciente(models.Model):
    TIPOS = [('estudiante', 'Estudiante'), ('docente', 'Docente')]
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    dni = models.CharField(max_length=8, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    tipo = models.CharField(max_length=15, choices=TIPOS)
    codigo_uncp = models.CharField(max_length=20)
    correo = models.EmailField()
    alergias = models.TextField(blank=True)

    def __str__(self):
        return f"{self.dni} - {self.apellidos}, {self.nombres}"


class Medico(models.Model):
    cmp = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=80)
    consultorio = models.CharField(max_length=40)
    horario_atencion = models.CharField(max_length=80, default='L-V 08:00-18:00, Sáb 08:00-13:00')

    def __str__(self):
        return f"Dr(a). {self.apellidos} ({self.especialidad})"


class CitaMedica(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='citas')
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='citas')
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    estado = models.CharField(max_length=15, choices=ESTADOS, default='pendiente')
    creado_en = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.paciente} con {self.medico}"