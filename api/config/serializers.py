from rest_framework import serializers
from paradigma.serializers.model_serializers import DynamicFieldsModelSerializer, RecursiveField
from .models import DefaultConfig

class DefaultConfigSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = DefaultConfig
        depth = 1
        fields = ('decimalesCant', 'decimalesChar', 'milesChar')
