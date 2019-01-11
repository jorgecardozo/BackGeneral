from ..models import Permisos
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User


def Exists(id=None, str_nombre=None):
    """
    Devuelve True o False de acuerdo a si existe o no.
    """
    if id != None:
        return Permisos.objects.filter(id=id).exists()
    elif str_nombre != None:
        return Permisos.objects.filter(nombre=str_nombre).exists()
    else:
        return False

def GetPermiso(id=None, str_nombre=None):
    """
    Devuelve el objeto del Permiso si existe, sino devuelve False
    """
    if id != None or str_nombre != None:
        if Exists(id, str_nombre):
            if id != None:
                return Permisos.objects.get(id=id)
            elif str_nombre != None:
                return Permisos.objects.get(nombre=str_nombre)
        else:
            return False
    else:
        return False
