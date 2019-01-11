from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist

from rest_framework.exceptions import AuthenticationFailed

from paradigma.objects.classes import DataTransferResultSet

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



def Login(username, password):
    """
    Obtiene el token de autentificacion a partir de un username/email y password
    """
    try:
        if User.objects.filter(username=username).exists():
            obj_user = authenticate(username=username, password=password)
            if obj_user != None:
                return GenerateToken(obj_user.pk)
            else:
                raise AuthenticationFailed('La contraseña es incorrecta.', '0000002')
        elif User.objects.filter(email=username).exists():
            username = User.objects.filter(email=username).first().username
            obj_user = authenticate(username=username, password=password)
            if obj_user != None:
                return GenerateToken(obj_user.pk)
            else:
                raise AuthenticationFailed('La contraseña es incorrecta.', '0000003')
        else:
            raise AuthenticationFailed('Los datos ingresados son incorrectos', '0000009')
    except Exception as ex:
        raise AuthenticationFailed('Los datos ingresados son incorrectos', '0000001')

def AuthCheck(token):
    """
    Devuelve si el token existe o expiro
    """
    if token != None:
        try:
            token = Token.objects.get(key=token)
            return token
        except:
            return False
    else:
        return False


def AuthCheckWithToken(token, password):
    """
    Devuelve si el token existe o expiro
    """
    if token != None:
        try:
            token = Token.objects.get(key=token)
            if authenticate(username=token.user.username, password=password) != None:
                return GenerateToken(token.user_id)
            else:
                DeleteToken(token.user_id)
                return False
        except:
            return False
    else:
        return False

def DeleteToken(user_id):
    """
    Eliminar el Token asociado a un usuario (si es que existe).
    """
    try:
        if user_id != None:
            token = Token.objects.filter(user_id=user_id)
            token.delete()
    except:
        pass
    
def GenerateToken(user_id):
    """
    Genera un token nuevo para el user_id
    """
    try:
        if user_id != None:
            user = User.objects.get(id=user_id)
            token, created = Token.objects.get_or_create(user = user)
            return token
    except:
        pass