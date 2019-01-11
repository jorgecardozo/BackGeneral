import json

#Responses
from paradigma.serializers.common import PermissionJsonResult, ValidJsonResult, InvalidJsonResult, ValidJsonResultSet, ValidationErrorJsonResult, CreatedJsonResult, NotFoundJsonResult

#Exceptions
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError, ValidationError, PermissionDenied
from rest_framework.serializers import ValidationError as SerializerValidationError

#auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes

#Paradigma Requests Parsers
from paradigma.serializers.request_serializers import DynamicRequestModel, DynamicRequestModelList
from paradigma.serializers.report_serializers import DynamicRequestModelReport

#App Controller
from ..controllers.controller_usuarios import List, Get, Create, Edit, Delete, Export

#App Serializers
from ..serializers import UserSerializer

@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated, ))
def list(request):
    try:
        if request.method == "GET":
            dto_validator = DynamicRequestModelList(request, UserSerializer)
            obj_result = List(dto_validator, request.user.is_superuser)
            return ValidJsonResult(obj_result.rows, obj_result.GetMeta())
        elif request.method == "POST":
            dto_serializer = UserSerializer(data=request.data)
            dto_serializer.is_valid(raise_exception=True)

            data = dto_serializer.validated_data
            perfil_data = data['perfil']
            data.pop('perfil', None)

            permisos_data = perfil_data['permisos']
            perfil_data.pop('permisos', None)

            grupos_data = perfil_data['grupos']
            perfil_data.pop('grupos', None)
            
            obj_result = Create(data, perfil_data, grupos_data, permisos_data)
            return CreatedJsonResult(obj_result)
    except FieldError as ex:
        print(ex)
        return InvalidJsonResult(ex.args)
    except FieldDoesNotExist as ex:
        print(ex)
        return InvalidJsonResult(ex.args)
    except ValidationError as ex:
        print(ex)
        return ValidationErrorJsonResult(ex.args)
    except SerializerValidationError as ex:
        print(ex)
        return ValidationErrorJsonResult(ex.args)
    except PermissionDenied as ex:
        return PermissionJsonResult(ex.args)
    except Exception as ex:
        print(ex)
        return InvalidJsonResult(ex.args)


@api_view(['GET','PATCH'])
@permission_classes((IsAuthenticated, ))
def perfil(request):
    try:
        return detail(request._request, request.user.id)
    except Exception as ex:
        print(ex)
        return InvalidJsonResult(ex.args)

@api_view(['GET','DELETE','PATCH'])
@permission_classes((IsAuthenticated, ))
def detail(request, id):
    try:
        id = int(id)
        if request.method == "GET":
            dto_validator = DynamicRequestModel(request, UserSerializer)
            obj_result = Get(id, dto_validator.fields, dto_validator.depth)
            if 'accesosDirectos' in obj_result:
                obj_result['accesosDirectos'] = json.loads(obj_result['accesosDirectos'])
            return ValidJsonResult(obj_result)
        elif request.method == "DELETE":
            Delete(id)
            return ValidJsonResult()
        elif request.method == "PATCH":
            
            if 'username' in request.data:
                request.data.pop('username', None)
            if 'email' in request.data:
                request.data.pop('email', None)
            if 'accesosDirectos' in request.data:
                request.data['accesosDirectos'] = json.dumps(request.data['accesosDirectos'])

            dto_serializer = UserSerializer(data=request.data, partial=True)
            dto_serializer.is_valid(raise_exception=True)
            
            data = dto_serializer.validated_data
            perfil_data = None
            permisos_data = None
            grupos_data = None

            if 'perfil' in data.keys():
                perfil_data = data.pop('perfil', None)

                if 'grupos' in perfil_data:
                    grupos_data = perfil_data.pop('grupos', None)

                if 'permisos' in perfil_data:
                    permisos_data = perfil_data.pop('permisos', None)

            obj_result = Edit(id, data, perfil_data, grupos_data, permisos_data)
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
        return PermissionJsonResult(ex.args)
    except Exception as ex:
        print(ex)
        return InvalidJsonResult(ex.args)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def getExportToken(request):
    dto_validator = DynamicRequestModelReport(request, UserSerializer)
    return dto_validator.ReportTokenResponse()

def export(request, token):
    dto_validator = DynamicRequestModelReport(request, UserSerializer, token)
    return Export(dto_validator)