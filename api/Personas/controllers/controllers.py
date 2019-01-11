from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from paradigma.objects.classes import DataTransferResultSet

from ..services.services import Exists
from ..serializers import PersonasSerializer
from ..models import Personas

from django.db.models import F, Value
from django.db.models.functions import Concat

from paradigma.utilities import list_reports

# Metodos
def List(dto_drml):
    db_query = Personas.objects
    int_total_rows = db_query.count()
    db_query = dto_drml.FilterList(db_query)
    db_query = dto_drml.SortList(db_query)
    int_total_rows_filtered = db_query.count()
    db_query = dto_drml.LimitList(db_query)
    
    serialized = PersonasSerializer(db_query, many=True, fields=(dto_drml.fields), depth=(dto_drml.depth))

    return DataTransferResultSet(serialized.data, int_total_rows_filtered, int_total_rows, dto_drml.page, dto_drml.pageSize)

def Get(id, fields = [], depth = None):
    if Exists(id):
        obj = Personas.objects.get(id=id)
        serializer = PersonasSerializer(obj, fields=(fields), depth=(depth))
        return serializer.data
    else:
        raise ObjectDoesNotExist(id)
    
def Create(data):
    obj = Personas(**data)
    obj.full_clean()
    obj.save()
    return Get(obj.id)

def Edit(id, data):
    if Exists(id):
        obj = Personas.objects.get(id=id)
        for field, value in data.items():
            setattr(obj, field, value)
        obj.full_clean()
        obj.save()
        return Get(obj.id)
    else:
        raise ObjectDoesNotExist(id)

def Delete(id):
    if Exists(id):
        Personas.objects.get(id=id).delete()
    else:
        raise ObjectDoesNotExist(id)
