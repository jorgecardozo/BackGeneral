from rest_framework import serializers
from collections import OrderedDict
from rest_framework.fields import get_error_detail, set_value

from rest_framework.fields import SkipField
from rest_framework.relations import Hyperlink, PKOnlyObject

from django.db.models import Q

class CommaSeparatedCharField(serializers.CharField):
    def to_representation(self, obj):
        if obj:
            return obj.split(',')
        else:
            return []

class FilterSerializer(serializers.Serializer):
    str_field = serializers.CharField()
    str_operator = serializers.CharField()
    str_value = serializers.CharField()
    is_not = serializers.BooleanField()
    is_or = serializers.BooleanField()

    def to_representation(self, data):
        return data

    def run_validation(self, data):
        return self.ParseStrFilter(data)

    def ParseStrFilter(self, _str):
        ret = dict()
        str_filter = ''
        ar_obj = _str.split('=')
        str_field_name = ar_obj[0].split('[')[0]
        str_operator = None

        is_not = False
        is_or = False

        
        if str_field_name[0:4] == 'or__':
            is_or = True
            str_field_name = str_field_name[4:]


        if '[' in ar_obj[0]:
            str_operator = ar_obj[0].split('[')[1].split(']')[0]
            if str_operator == "not_in":
                is_not = True
                str_operator = "in"

        str_filter = str_field_name
        if str_operator != None:
            str_filter += "__" + str_operator
        value = ar_obj[1]

        fields = self._writable_fields
        for field in fields:
            if field.field_name == "str_field":
                set_value(ret, field.source_attrs, str_field_name)
            elif field.field_name == "str_value":
                set_value(ret, field.source_attrs, value)
            elif field.field_name == "str_operator":
                set_value(ret, field.source_attrs, str_operator)
            elif field.field_name == "is_not":
                set_value(ret, field.source_attrs, is_not)
            elif field.field_name == "is_or":
                set_value(ret, field.source_attrs, is_or)
        return ret

    def to_internal_value(self, data):
        return [self.ParseStrFilter(obj) for obj in data]

    def GetFilter(data):
        is_not = data['is_not']
        str_field = data['str_field']
        str_operator = data['str_operator']
        str_value = data['str_value']
        
        str_filter = str_field
        if str_operator != None:
            str_filter += "__" + str_operator
        
        if ',' in str_value:
            str_value = str_value.replace('[','').replace(']','').split(',')

        if is_not:
            return Q(~Q(**{str_filter: str_value}))
        else:
            return Q(**{str_filter: str_value})

class RequestListSerializer(serializers.Serializer):
    q = serializers.CharField(required=False)
    page = serializers.IntegerField(required=False)
    pageSize = serializers.IntegerField(required=False)
    fields = CommaSeparatedCharField(required=False)
    sort = CommaSeparatedCharField(required=False)
    depth = serializers.IntegerField(required=False)
    filters = serializers.ListField(child=FilterSerializer(),required=False)

    def __init__(self, request, serializer):
        reserved_field_names = [str(field) for field in self.fields]

        request_data = request.GET

        data = {}
        request_data._mutable = True
        
        filters = []
        for k, v in request_data.items():
            if k in reserved_field_names:
                data[k] = v
            else:
                if ',' in v:
                    filters.append(k.replace(',','') + "=[" + v + "]")
                else:
                    filters.append(k.replace(',','') + "=" + v)
        
        if filters != []:
            data['filters'] = filters

        if 'pageSize' not in data:
            data['pageSize'] = 30
        
        if 'page' not in data:
            data['page'] = 0
        
        args = {}
        kwargs = {"data": data}

        super(RequestListSerializer, self).__init__(*args, **kwargs)

        self.is_valid()
        self._validate(serializer)
        


    def _validate(self, serializer):
        valid_fields = [field for field in serializer().get_fields()]

        if 'fields' in self.data:
            for field in self.data['fields']:
                if field not in valid_fields:
                    raise Exception("El campo " + field + " no se encuentra asociado a este recurso.")

        if 'sort' in self.data:
            for field in self.data['sort']:
                if field.replace('-', '') not in valid_fields:
                    raise Exception("El campo de ordenamiento " + field + " no se encuentra asociado a este recurso.")

        if 'filters' in self.data:
            for field in self.data['filters']:
                if field['str_field'] not in valid_fields:
                    raise Exception("El filtro " + field['str_field'] + " no se encuentra asociado a este recurso.")

    

class RequestModelSerializer(serializers.Serializer):
    fields = CommaSeparatedCharField(required=False)
    depth = serializers.IntegerField(required=False)

    def __init__(self, request, serializer):
        reserved_field_names = [str(field) for field in self.fields]

        ar_fields = request.GET.get('fields', None)
        str_depth = request.GET.get('depth', None)

        data = {}
        if ar_fields != None:
            data['fields'] = ar_fields
            
        if str_depth != None:    
            data['depth'] = int(str_depth)

        args = {}
        kwargs = {"data": data}

        super(RequestModelSerializer, self).__init__(*args, **kwargs)

        self.is_valid()
        self._validate(serializer)
        
    def _validate(self, serializer):
        valid_fields = [field for field in serializer().get_fields()]
        if 'fields' in self.data:
            for field in self.data['fields']:
                if field not in valid_fields:
                    raise Exception("El campo " + field + " no se encuentra asociado a este recurso.")




class DynamicRequestModel:
    def __init__(self, request, modelSerializer):
        serializer_request = RequestModelSerializer(request, modelSerializer)
        data = serializer_request.data

        if 'fields' in data:
            self.fields = data['fields']
        else:
            self.fields = []
        
        if 'depth' in data:
            self.depth = data['depth']
        else:
            self.depth = None


class DynamicRequestModelList:
    def __init__(self, request, modelSerializer):
        serializer_request = RequestListSerializer(request, modelSerializer)
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

    def GetFilter(self):
        db_filter = None
        for _filter in self.filters:
            if db_filter != None:
                if _filter['is_or']:
                    db_filter = db_filter | FilterSerializer.GetFilter(_filter)
                else:
                    db_filter = db_filter & FilterSerializer.GetFilter(_filter)
            else:
                db_filter = FilterSerializer.GetFilter(_filter)
        return db_filter

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
        int_start = self.page * self.pageSize
        int_length = self.pageSize * (self.page + 1)
        return db_query[int_start:int_length]
