from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, PermissionDenied

from paradigma.objects.classes import DataTransferResultSet

from .serializers import DefaultConfigSerializer
from .models import DefaultConfig

def Get(fields = [], depth = 0):
    obj = DefaultConfig.objects.get(id=1)
    serializer = DefaultConfigSerializer(obj, fields=(fields), depth=(depth))
    return serializer.data

def Edit(data):
    obj = DefaultConfig.objects.get(id=1)
    for field, value in data.items():
        setattr(obj, field, value)
    obj.save()
    return Get()
