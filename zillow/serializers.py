from zillow.models import Property, PropertyType
from rest_framework import serializers

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = '__all__'
        read_only_fields = 'created_at'

class PropertyTypeSerializer(serializers.ModelSerializer):
    properties = PropertySerializer(many=True, read_only=True)
    class Meta:
        model = PropertyType
        fields = '__all__'