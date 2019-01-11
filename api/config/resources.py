import json

#Responses
from paradigma.serializers.common import ValidJsonResult, InvalidJsonResult, ValidJsonResultSet, ValidationErrorJsonResult, CreatedJsonResult, NotFoundJsonResult

#Exceptions
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError, ValidationError
from rest_framework.serializers import ValidationError as SerializerValidationError

#auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes

#Paradigma Requests Parsers
from paradigma.serializers.request_serializers import DynamicRequestModel

#App Controller
from .controller import Get, Edit

#App Serializers
from .serializers import DefaultConfigSerializer

@api_view(['GET','PUT'])
@permission_classes((IsAuthenticated, ))
def detail(request):
    try:
        if request.method == "GET":
            dto_validator = DynamicRequestModel(request, DefaultConfigSerializer)
            obj_result = Get(dto_validator.fields, dto_validator.depth)
            return ValidJsonResult(obj_result)
        elif request.method == "PUT":
            dto_serializer = DefaultConfigSerializer(data=request.data, check_unique=False)
            dto_serializer.is_valid(raise_exception=True)
            data = dto_serializer.validated_data

            obj_result = Edit(data)
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
    except Exception as ex:
        return InvalidJsonResult(ex.args)