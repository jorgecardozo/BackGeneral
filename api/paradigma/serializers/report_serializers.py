from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import get_error_detail, set_value

from rest_framework.fields import SkipField
from rest_framework.relations import Hyperlink, PKOnlyObject

from django.db.models import Q

import json, base64

from paradigma.serializers.common import ValidJsonResult
from paradigma.utilities.gzip import gunzip_bytes_obj, gzip_str


class FilterSerializer(serializers.Serializer):
    id = serializers.CharField()
    lookup = serializers.CharField()
    input = serializers.CharField()
    is_not = serializers.BooleanField(required=False, default=False)

    def __init__(self, *args, **kwargs):
        print(args)
        print(kwargs)
        super(FilterSerializer, self).__init__(*args, **kwargs)
        
    def GetFilter(data):
        print("filters")
        print(data)
        is_not = False
        if 'is_not' in data:
            is_not = True
        str_field = data['id']
        str_operator = data['lookup']
        str_value = data['input']
        
        str_filter = str_field
        if str_operator != None:
            str_filter += "__" + str_operator
        
        if ',' in str_value:
            str_value = str_value.replace('[','').replace(']','').split(',')

        if is_not:
            return Q(~Q(**{str_filter: str_value}))
        else:
            return Q(**{str_filter: str_value})


class ColumnSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    width = serializers.FloatField()


class RequestListSerializer(serializers.Serializer):
    partial = True

    q = serializers.CharField(required=False)
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    fields = ColumnSerializer(many=True)
    sort = serializers.ListField(child=serializers.CharField(), required=False)
    depth = serializers.IntegerField(required=False)
    filters = FilterSerializer(many=True, required=False)


    format = serializers.CharField(required = False)
    mode = serializers.IntegerField(required = False)
    landscape = serializers.BooleanField(required=False)


    def __init__(self, data, serializer):
        
        args = {}
        kwargs = {"data": data}

        super(RequestListSerializer, self).__init__(*args, **kwargs)

        self.is_valid()
        self._validate(serializer)
        


    def _validate(self, serializer):
        valid_fields = [field for field in serializer().get_fields()]

        if 'fields' in self.data:
            for field in self.data['fields']:
                if field['id'] not in valid_fields:
                    raise Exception("El campo " + field + " no se encuentra asociado a este recurso.")

        if 'sort' in self.data:
            for field in self.data['sort']:
                if field.replace('-', '') not in valid_fields:
                    raise Exception("El campo de ordenamiento " + field + " no se encuentra asociado a este recurso.")

        if 'filters' in self.data:
            for field in self.data['filters']:
                if field['id'] not in valid_fields:
                    raise Exception("El filtro " + field['str_field'] + " no se encuentra asociado a este recurso.")

class DynamicRequestModelReport:

    def __init__(self, request, modelSerializer, reporttoken=None):
        data = None
        _dict = {}
        if reporttoken != None:
            _dict = DynamicRequestModelReport.GetDictionaryFromToken(reporttoken)
            data = _dict
        else:
            serializer_request = RequestListSerializer(request.data, modelSerializer)
            data = serializer_request.data

        if 'q' in data:
            self.q = data['q']
        else:
            self.q = None

        if 'page' in data:
            self.page = data['page']
        else:
            self.page = 0

        if 'pageSize' in data:
            self.pageSize = data['pageSize']
        else:
            self.pageSize = 30
        
        if 'sort' in data:
            self.sort = data['sort']
        else:
            self.sort = []
        
        if 'filters' in data:
            self.filters = data['filters']
        else:
            self.filters = []

        if 'fields' in data:
            self.fields = data['fields']
        else:
            self.fields = []
        
        if 'depth' in data:
            self.depth = data['depth']
        else:
            self.depth = None

        if 'format' in data:
            self.format = data['format']
        else:
            self.format = None

        if 'mode' in data:
            self.mode = data['mode']
        else:
            self.mode = None

        if 'landscape' in data:
            if data['landscape'] == False:
                self.landscape = False
            else:
                self.landscape = True
        else:
            self.landscape = False

    def ReportTokenResponse(self):
        _dict = self.__dict__
        _str_dict = json.dumps(_dict)
        _gziped_str = gzip_str(_str_dict)
        _encoded = base64.b64encode(_gziped_str).decode("utf-8") 
        return ValidJsonResult({'tokenreport':_encoded})

    def GetDictionaryFromToken(reporttoken):
        _gziped_str = base64.b64decode(reporttoken)
        _str_dict = gunzip_bytes_obj(_gziped_str)
        _dict = json.loads(_str_dict)
        
        return _dict

    def GetFilter(self):
        if not self.mode == 3:
            db_filter = None
            for _filter in self.filters:
                if db_filter != None:
                    db_filter = db_filter & FilterSerializer.GetFilter(_filter)
                else:
                    db_filter = FilterSerializer.GetFilter(_filter)
            return db_filter
        else:
            return None

    def FilterList(self, db_query):
        db_filter = self.GetFilter()
        if db_filter != None:
            return db_query.filter(db_filter)
        else:
            return db_query

    def SortList(self, db_query):
        if self.sort != []:
            return db_query.order_by(*self.sort).distinct()
        else:
            return db_query.order_by('-pk').distinct()

    def LimitList(self, db_query):
        if not self.mode == 3:
            int_start = self.page * self.pageSize
            int_length = self.pageSize * (self.page + 1)
            return db_query[int_start:int_length]
        else:
            return db_query