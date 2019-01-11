from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, PermissionDenied

from paradigma.objects.classes import DataTransferResultSet
from datetime import datetime

from ..services.services_usuarios import Exists
from ..serializers import UserSerializer
from ..models import User, Perfil

from django.db.models import F, Value
from django.db.models.functions import Concat

from paradigma.utilities import list_reports


def List(dto_drml, superadmin=False):
    db_query = User.objects
    
    if not superadmin:
        db_query = db_query.exclude(id=1)

    db_query = db_query.annotate(
        apellido_nombre = Concat(F('last_name'), Value(' '), F('first_name'))
    )
    int_total_rows = db_query.count()
    db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    int_total_rows_filtered = db_query.count()
    db_query = dto_drml.LimitList(db_query)
    
    serialized = UserSerializer(db_query, many=True, fields=(dto_drml.fields), depth=(dto_drml.depth))

    return DataTransferResultSet(serialized.data, int_total_rows_filtered, int_total_rows, dto_drml.page, dto_drml.pageSize)

def Get(id, fields = [], depth = 0):
    if Exists(id):
        obj = User.objects.get(id=id)
        serializer = UserSerializer(obj, fields=(fields), depth=(depth))
        return serializer.data
    else:
        raise ObjectDoesNotExist(id)
    
def Create(data, perfil_data, grupos_data, permisos_data):
    obj = User(**data)
    obj.set_password(data['password'])
    obj.save()

    perfil = Perfil(**perfil_data)
    perfil.user = obj
    perfil.save()

    perfil.permisos.set(permisos_data)
    perfil.save()

    perfil.grupos.set(grupos_data)
    perfil.save()
    return Get(obj.id)

def Edit(id, data, perfil_data, grupos_data, permisos_data):
    if Exists(id):
        obj = User.objects.get(id=id)
        for field, value in data.items():
            if field != 'password':
                setattr(obj, field, value)
        if 'password' in data:
            if data['password'] != None:
                obj.set_password(data['password'])
        obj.save()

        if perfil_data != None:
            for field, value in perfil_data.items():
                setattr(obj.perfil, field, value)
            obj.perfil.save()

        if grupos_data != None:
            obj.perfil.grupos.set(grupos_data)
            obj.perfil.save()
        
        if permisos_data != None:
            print(permisos_data)
            obj.perfil.permisos.set(permisos_data)
            obj.perfil.save()

        return Get(obj.id)
    else:
        raise ObjectDoesNotExist(id)

def Delete(id):
    if Exists(id):
        if id != 1:
            User.objects.get(id=id).delete()
        else:
            raise PermissionDenied(id)
    else:
        raise ObjectDoesNotExist(id)

def Export(dto_drml):
    db_query = User.objects

    db_query = db_query.annotate(
        apellido_nombre = Concat(F('last_name'), Value(' '), F('first_name'))
    )
    if dto_drml.mode != 3:
        db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    if dto_drml.mode != 3:
        db_query = dto_drml.LimitList(db_query)
    
    fields = [field['id'] for field in dto_drml.fields]

    serialized = UserSerializer(db_query, many=True, fields=(fields), depth=(dto_drml.depth))

    _data = serialized.data

    for _d in _data:
        for key in _d.keys():
            if key == "date_joined":
                _d[key] = datetime.strptime(_d["date_joined"],'%Y-%m-%dT%H:%M:%S.%f').strftime('%d-%m-%Y')

    print(_data)
    return list_reports.file_default_export(_data,'Usuarios',dto_drml)          
