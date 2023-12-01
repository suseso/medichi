from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Persona(models.Model):
    nombre = models.CharField(max_length=30, verbose_name="nombre")
    apellido = models.CharField(max_length=30, verbose_name="apellido")
    email = models.EmailField(max_length=150, verbose_name="email") 
    dni = models.PositiveIntegerField(verbose_name="dni", unique=True)

    def clean_dni(self):
        if not (0 < self.cleaned_data['dni'] <= 99999999):
            raise ValidationError("El Dni debe ser un numero positivo de 8 digitos")
        return self.cleaned_data['dni']

    class Meta:
        abstract = True

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def __str__(self):
        return self.nombre_completo()


class Especialidades(models.Model):
    especialidad = models.CharField(max_length=150, verbose_name=("especialidad"), unique=True)
    
    
    def __str__(self):
        return self.especialidad


class Plan(models.Model):
    plan_select = [
        (1, "Plan 300"),
        (2, "Plan 400"),
        (3, "Plan Platinum"), 
    ]   
    plan = models.IntegerField(choices=plan_select)
    def __str__(self):
        for value, name in self.plan_select:
            if value == self.plan:
                return name



class Afiliado(Persona):
    numeroAfiliado = models.CharField(max_length=100, verbose_name="numeroAfiliado")
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)


class Profesional(Persona):
    matricula = models.IntegerField(verbose_name="matricula")
    cuit = models.IntegerField(verbose_name="cuit")
    especialidades = models.ManyToManyField(Especialidades, related_name='especialidades')
    

    def __str__(self):
        return self.nombre_completo()

    def especialidades_list(self):
        return ', '.join(especialidad.especialidades for especialidad in self.especialidades.all())
 
#01-11-2023

class CrearTurno(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    profesional = models.ForeignKey('Profesional', on_delete=models.PROTECT)
    especialidades = models.ManyToManyField('Especialidades', related_name='specialidades')
    disponible = models.BooleanField(default=True)
    afiliado = models.ForeignKey('Afiliado', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        lista_especialidades = ", ".join([especialidad.especialidad for especialidad in self.especialidades.all()])
        return f'Turno el {self.fecha} a las {self.hora} con {self.profesional.nombre_completo()} en {lista_especialidades}'

