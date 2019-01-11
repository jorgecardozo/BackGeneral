from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from paradigma.objects.classes import DataTransferResultSet

from ..services.services_permisos import Exists
from ..serializers import PermisosSerializer
from ..models import Permisos

from django.db.models import F, Value
from django.db.models.functions import Concat

from paradigma.utilities import list_reports


def List(dto_drml):
    db_query = Permisos.objects
    int_total_rows = db_query.count()
    db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    int_total_rows_filtered = db_query.count()
    db_query = dto_drml.LimitList(db_query)
    
    serialized = PermisosSerializer(db_query, many=True, fields=(dto_drml.fields), depth=(dto_drml.depth))

    return DataTransferResultSet(serialized.data, int_total_rows_filtered, int_total_rows, dto_drml.page, dto_drml.pageSize)

def Get(id, fields = [], depth = None):
    if Exists(id):
        obj = Permisos.objects.get(id=id)
        serializer = PermisosSerializer(obj, fields=(fields), depth=(depth))
        return serializer.data
    else:
        raise ObjectDoesNotExist(id)
    
def Create(data):
    obj = Permisos(**data)
    obj.full_clean()
    obj.save()
    return Get(obj.id)

def Edit(id, data):
    if Exists(id):
        obj = Permisos.objects.get(id=id)
        for field, value in data.items():
            setattr(obj, field, value)
        obj.full_clean()
        obj.save()
        return Get(obj.id)
    else:
        raise ObjectDoesNotExist(id)

def Delete(id):
    if Exists(id):
        Permisos.objects.get(id=id).delete()
    else:
        raise ObjectDoesNotExist(id)

def Export(dto_drml):
    db_query = Permisos.objects
    if dto_drml.mode != 3:
        db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    if dto_drml.mode != 3:
        db_query = dto_drml.LimitList(db_query)
    
    fields = [field['id'] for field in dto_drml.fields]

    serialized = PermisosSerializer(db_query, many=True, fields=(fields), depth=(dto_drml.depth))

    _data = serialized.data

    return list_reports.file_default_export(_data,'Permisos',dto_drml)        
