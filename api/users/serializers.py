from rest_framework import serializers
from paradigma.serializers.model_serializers import DynamicFieldsModelSerializer, RecursiveField
from .models import User, Perfil, Permisos, Grupos
from rest_framework.validators import UniqueValidator
import json

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class AuthSerializer(serializers.Serializer):
    token = serializers.CharField()

class TokenPasswordSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField()

class PermisosSerializer(DynamicFieldsModelSerializer):
    id = serializers.ReadOnlyField()
    permisos = RecursiveField(many=True, read_only=True, source='permisos_set')

    padre_id = serializers.PrimaryKeyRelatedField(many=False, required=False, allow_null=True, queryset=Permisos.objects.all(), source='padre')
    permisos_id = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=Permisos.objects.all(), source='permisos_set')

    class Meta:
        model = Permisos
        depth = 1
        fields = ('id', 'nombre', 'descripcion', 'padre', 'padre_id', 'permisos', 'permisos_id')
        read_only_fields = ('padre', 'permisos')


class GruposSerializer(DynamicFieldsModelSerializer):
    id = serializers.ReadOnlyField()

    permisos_id = serializers.PrimaryKeyRelatedField(many=True, required=False, allow_null=True, queryset=Permisos.objects.all(), source='permisos')

    class Meta:
        model = Grupos
        depth = 1
        fields = ('id', 'nombre', 'permisos', 'permisos_id')
        read_only_fields = ('permisos', )


class PerfilSerializer(DynamicFieldsModelSerializer):
    grupos = GruposSerializer(many=True)
    permisos = PermisosSerializer(many=True, required=False, read_only=False)

    class Meta:
        model = Perfil
        fields = ('permisos', 'grupos', 'accesosDirectos')


class UserSerializer(DynamicFieldsModelSerializer):
    accesosDirectos = serializers.CharField(source='perfil.accesosDirectos', required=False)
    password = serializers.CharField(write_only=True)
    apellido_nombre = serializers.CharField(read_only=True)
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    grupos = GruposSerializer(read_only=True, allow_empty=True, many=True, source='perfil.grupos')
    grupos_id = serializers.PrimaryKeyRelatedField(write_only=True, many=True, allow_empty=True, queryset=Grupos.objects, source='perfil.grupos')
    
    permisos = PermisosSerializer(read_only=True, allow_empty=True, many=True, source='perfil.permisos')
    permisos_id = serializers.PrimaryKeyRelatedField(write_only=True, many=True, allow_empty=True, queryset=Permisos.objects, source='perfil.permisos')

    class Meta:
        model = User
        fields = ('id', 'accesosDirectos', 'grupos', 'grupos_id', 
                  'permisos', 'permisos_id', 'username', 
                  'apellido_nombre', 'email', 'password', 'first_name', 
                  'last_name', 'date_joined', 'is_active')