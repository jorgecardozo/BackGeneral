from django.db import models

from django.contrib.auth.models import User


class Permisos(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    descripcion = models.CharField(max_length=200, blank=False, null=False)
    padre = models.ForeignKey("self", null=True, blank=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.nombre

class Grupos(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    permisos = models.ManyToManyField(Permisos)
    
    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    permisos = models.ManyToManyField(Permisos)
    grupos = models.ManyToManyField(Grupos)
    accesosDirectos = models.TextField(blank=False, default="[]")