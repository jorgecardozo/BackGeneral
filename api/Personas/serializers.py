from paradigma.serializers.model_serializers import DynamicFieldsModelSerializer, RecursiveField
from .models import Personas
from rest_framework import serializers

class PersonasSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Personas
        fields = ('id', 'nombre', 'apellido', 'tipoDocumento', 'documento', 'email')

