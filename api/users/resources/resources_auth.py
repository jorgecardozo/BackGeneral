import json

#Responses
from paradigma.serializers.common import ValidJsonResult, InvalidJsonResult, AuthenticationFailedJsonResult

#Exceptions
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist, FieldError, ValidationError
from rest_framework.serializers import ValidationError as SerializerValidationError

#auth
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes
from rest_framework.exceptions import AuthenticationFailed
#Paradigma Requests Parsers
from paradigma.serializers.request_serializers import DynamicRequestModel, DynamicRequestModelList

#App Controller
from ..controllers.controller_auth import Login, AuthCheck, DeleteToken, AuthCheckWithToken, GenerateToken

#App Serializers
from ..serializers import LoginSerializer, AuthSerializer, TokenPasswordSerializer
from ..services.services_usuarios import GetPermisos

from config.controller import Get as GetConfig

@api_view(['POST'])
@permission_classes((AllowAny, ))
def login(request):
    try:
        dto_validator = LoginSerializer(data=request.data)
        dto_validator.is_valid(raise_exception=True)
        obj_token = Login(**dto_validator.data)
        return ValidJsonResult({
            'displayname': obj_token.user.last_name + ", " + obj_token.user.first_name,
            'token': obj_token.key, 
            'permisos': GetPermisos(obj_token.user_id),
            'configuraciones': GetConfig()
        })
    except AuthenticationFailed as ex:
        print(ex)
        return AuthenticationFailedJsonResult({ 'error': ex.detail })
    except Exception as ex:
        print(ex)
        return InvalidJsonResult(ex.args)

@api_view(['POST'])
@permission_classes((AllowAny, ))
def auth_check(request):
    try:
        dto_validator = AuthSerializer(data=request.data)
        dto_validator.is_valid(raise_exception=True)
        obj_token = AuthCheck(**dto_validator.data)
        if obj_token == False:
            return ValidJsonResult({'exists': obj_token})
        return ValidJsonResult({
            'displayname': obj_token.user.last_name + ", " + obj_token.user.first_name, 
            'exists': True,
            'config': GetConfig()
        })
    except FieldError as ex:
        return InvalidJsonResult(ex.args)
    except Exception as ex:
        return InvalidJsonResult(ex.args)

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def auth_check_with_token(request):
    try:
        dto_validator = TokenPasswordSerializer(data=request.data, partial=True)
        dto_validator.is_valid(raise_exception=True)
        obj_token = AuthCheckWithToken(**dto_validator.data)
        return ValidJsonResult({
            'displayname': obj_token.user.last_name + ", " + obj_token.user.first_name,
            'token': obj_token.key, 
            'permisos': GetPermisos(obj_token.user_id),
            'config': GetConfig()
        })
    except FieldError as ex:
        return InvalidJsonResult(ex.args)
    except Exception as ex:
        return InvalidJsonResult(ex.args)

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def clear_token(request):
    try:
        DeleteToken(request.user.id)
        new_token = GenerateToken(request.user.id)
        return ValidJsonResult({ 
            'displayname': new_token.user.last_name + ", " + new_token.user.first_name,
            'token': new_token.key 
        })
    except:
        pass

@api_view(['GET'])
@authentication_classes((TokenAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def get_permissions(request):
    return ValidJsonResult({
        'permisos': GetPermisos(request.user.id)
    })

@api_view(['GET'])
@permission_classes((AllowAny, ))
def logout(request):
    try:
        DeleteToken(request.user.id)
    except:
        pass
    return ValidJsonResult()