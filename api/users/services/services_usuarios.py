from ..models import User, Permisos
from .services_permisos import GetPermiso

from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q, OuterRef, Subquery, Count

def Exists(id):
    """
    Devuelve True o Falso de acuerdo a si existe o no.
    """
    return User.objects.filter(id=id).exists()

def GetPerfil(id):
    """
    Devuelve el Perfil del Usuario. Si es que el Usuario existe, sino devuelve False.
    """
    if Exists(id):
        return User.objects.get(id=id).perfil
    else:
        return False

def HasPermiso(id, permiso_id=None, permiso_nombre=None):
    """
    Devuelve True o Falso de acuerdo a si el user tiene permiso o no. Si el user no existe, también devuelve False.
    """
    obj_perfil = GetPerfil(id)
    if obj_perfil != False:
        if obj_perfil.user.is_superuser:
            return True
            
        obj_permiso = GetPermiso(permiso_id, permiso_nombre)
        if obj_permiso != False:
            if obj_perfil.permisos.filter(id=obj_permiso.id).exists():
                return True
            elif obj_perfil.grupos.filter(permisos__id=obj_permiso.id).exists():
                return True
            else:
                return False
        else:
            return False
    else:
        return False

def HasAnyPermiso(id, ar_ids=None, ar_nombres=None):
    """
    Devuelve True o Falso de acuerdo a si el user tiene alguno de los permisos o no. Si el user no existe, también devuelve False.
    """
    obj_perfil = GetPerfil(id)
    if obj_perfil != False:
        if ar_ids != None and (obj_perfil.permisos.filter(id__in=ar_ids).exists() or obj_perfil.grupos.filter(permisos__id__in=ar_ids).exists()):
            return True
        elif ar_nombres != None and (obj_perfil.permisos.filter(nombre__in=ar_nombres).exists() or obj_perfil.grupos.filter(permisos__nombre__in=ar_nombres).exists()):
            return True
        else:
            return False
    else:
        return False

def GetPermisos(id):
    obj_perfil = GetPerfil(id)
    if obj_perfil != False:
        if obj_perfil.user.is_superuser:
            db_subquery = Permisos.objects.filter(padre_id=OuterRef('id')).values('padre_id').annotate(
                count=Count('id')
            ).values('count')
            db_query = Permisos.objects.annotate(
                ccount=Subquery(db_subquery)
            ).filter(Q(padre_id__isnull=False) | Q(ccount__isnull=True) | Q(ccount=0)).values_list('nombre', flat=True)
            ar_permisos = list(db_query)
            ar_permisos.append("superadmin")
            return ar_permisos
        else:
            ar_permisos = []
            ar_permisos = list(obj_perfil.permisos.values_list('nombre', flat=True))
            for permiso in obj_perfil.grupos.values_list('permisos__nombre', flat=True):
                ar_permisos.append(permiso)
            return ar_permisos
    else:
        return []

def JsonResult(status, meta = None, data = None, errors = None):
    obj = dict()
    if meta != None:
        obj["meta"] = meta
    if data != None:
        obj["data"] = data
    if errors != None:
        obj["errors"] = errors
    response = Response(obj, status=status)
    return response

def CheckPermisos(str_nombres):
    """
    Se utiliza como decorador en las vistas/endpoints de la api, para denegar/permitir el acceso/visualización de las mismas.
    """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if request.user.is_superuser or HasAnyPermiso(request.user.id, None, str_nombres.split(',')):
                return view_method(request, *args, **kwargs)
            else:
                meta = {
                    'allowed': False,
                    'message': "No tiene permisos para realizar esta acción."
                }
                return JsonResult(status.HTTP_401_UNAUTHORIZED, meta, None, None)
        return _arguments_wrapper
    return _method_wrapper