from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Car, Cargo, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  # Serialize all fields of the Location model


class CargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'
        list_editable = ['weight', 'description']

    def update(self, instance, validated_data):
        instance.weight = validated_data.get('weight', instance.weight)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        return instance
        

class CarSerializer(serializers.ModelSerializer):
    unique_number = serializers.ReadOnlyField()
    payload_capacity = serializers.IntegerField(min_value=1, max_value=1000)
    
    class Meta:
        model = Car
        fields = '__all__'
    
    def update(self, instance, validated_data):
        """
        Update a Car, by replacing the current_location with the new one
        """
        instance.payload_capacity = validated_data.get("payload_capacity", instance.payload_capacity)
        instance.unique_number = validated_data.get("unique_number", instance.unique_number)
        instance.current_location = validated_data.pop("current_location", self.fields["current_location"])
        instance.save()

        return instance
