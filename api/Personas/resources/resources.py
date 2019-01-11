import json

#Responses
from paradigma.serializers.common import ValidJsonResult, InvalidJsonResult, ValidJsonResultSet, ValidationErrorJsonResult, CreatedJsonResult, NotFoundJsonResult, PermissionJsonResult
from django.core.exceptions import PermissionDenied

#Exceptions
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError, ValidationError
from rest_framework.serializers import ValidationError as SerializerValidationError

#auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes

#Paradigma Requests Parsers
from paradigma.serializers.request_serializers import DynamicRequestModel, DynamicRequestModelList

from paradigma.serializers.report_serializers import DynamicRequestModelReport

#App Controller
from ..controllers.controllers import List, Get, Create, Edit, Delete

#App Serializers
from ..serializers import PersonasSerializer

@api_view(['GET', 'POST'])
@permission_classes((AllowAny, ))
def list(request):
    try:
        if request.method == "GET":
            dto_validator = DynamicRequestModelList(request, PersonasSerializer)
            obj_result = List(dto_validator)
            return ValidJsonResult(obj_result.rows, obj_result.GetMeta())
        elif request.method == "POST":
            dto_serializer = PersonasSerializer(data=request.data)
            dto_serializer.is_valid(raise_exception=True)
            data = dto_serializer.validated_data

            obj_result = Create(data)
            return CreatedJsonResult(obj_result)
    except FieldError as ex:
        return InvalidJsonResult(ex.args)
    except FieldDoesNotExist as ex:
        return InvalidJsonResult(ex.args)
    except ValidationError as ex:
        return ValidationErrorJsonResult(ex.args)
    except SerializerValidationError as ex:
        return ValidationErrorJsonResult(ex.args)
    except PermissionDenied as ex:
        return PermissionJsonResult()
    except Exception as ex:
        return InvalidJsonResult(ex.args)

@api_view(['GET','PUT','DELETE'])
@permission_classes((AllowAny, ))
def detail(request, id):
    try:
        if request.method == "GET":
            dto_validator = DynamicRequestModel(request, PersonasSerializer)
            obj_result = Get(id, dto_validator.fields, dto_validator.depth)
            return ValidJsonResult(obj_result)
        elif request.method == "DELETE":
            Delete(id)
            return ValidJsonResult()
        elif request.method == "PUT":
            dto_serializer = PersonasSerializer(data=request.data, check_unique=False)
            dto_serializer.is_valid(raise_exception=True)
            data = dto_serializer.validated_data
            
            obj_result = Edit(id, data)
            return ValidJsonResult(obj_result)
        else:
            pass
    except ObjectDoesNotExist as ex:
        return NotFoundJsonResult(ex.args)
    except FieldDoesNotExist as ex:
        return InvalidJsonResult(ex.args)
    except ValidationError as ex:
        return ValidationErrorJsonResult(ex.args)
    except SerializerValidationError as ex:
        return ValidationErrorJsonResult(ex.args)
    except PermissionDenied as ex:
        return PermissionJsonResult()
    except Exception as ex:
        return InvalidJsonResult(ex.args)