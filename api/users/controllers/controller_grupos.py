from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from paradigma.objects.classes import DataTransferResultSet

from ..services.services_grupos import Exists
from ..serializers import GruposSerializer
from ..models import Grupos

from paradigma.utilities import list_reports

from django.db.models import F, Value
from django.db.models.functions import Concat

def List(dto_drml, superadmin=False):
    db_query = Grupos.objects
    if not superadmin:
        db_query = db_query.exclude(id=1)
        
    int_total_rows = db_query.count()
    db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    int_total_rows_filtered = db_query.count()
    db_query = dto_drml.LimitList(db_query)
    
    serialized = GruposSerializer(db_query, many=True, fields=(dto_drml.fields), depth=(dto_drml.depth))

    return DataTransferResultSet(serialized.data, int_total_rows_filtered, int_total_rows, dto_drml.page, dto_drml.pageSize)

def Get(id, fields = [], depth = None):
    if Exists(id):
        obj = Grupos.objects.get(id=id)
        serializer = GruposSerializer(obj, fields=(fields), depth=(depth))
        return serializer.data
    else:
        raise ObjectDoesNotExist(id)
    
def Create(data, permisos_data):
    obj = Grupos(**data)
    obj.full_clean()
    obj.save()
    if permisos_data != None:
        obj.permisos.set(permisos_data)
        obj.save()
    return Get(obj.id)

def Edit(id, data, permisos_data):
    if Exists(id):
        print(data, permisos_data)
        obj = Grupos.objects.get(id=id)
        for field, value in data.items():
            setattr(obj, field, value)
        obj.save()
        if permisos_data != None:
            obj.permisos.set(permisos_data)
            obj.save()
        return Get(obj.id)
    else:
        raise ObjectDoesNotExist(id)

def Delete(id):
    if Exists(id):
        Grupos.objects.get(id=id).delete()
    else:
        raise ObjectDoesNotExist(id)

def Export(dto_drml):
    db_query = Grupos.objects
    if dto_drml.mode != 3:
        db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    if dto_drml.mode != 3:
        db_query = dto_drml.LimitList(db_query)
    
    fields = [field['id'] for field in dto_drml.fields]

    serialized = GruposSerializer(db_query, many=True, fields=(fields), depth=(dto_drml.depth))

    _data = serialized.data

    return list_reports.file_default_export(_data,'Grupos',dto_drml)        
