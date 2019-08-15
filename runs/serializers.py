from rest_framework import serializers
from .models import Run, Gear


class GearSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gear
        fields = (
            'pk',
            'name',
            'start_distance',
            'start_units',
            'date_added',
            'date_retired',)
        extra_kwargs = {
            'pk': {'read_only': True}}


class RunSerializer(serializers.ModelSerializer):
    gear = GearSerializer(read_only=True)

    class Meta:
        model = Run
        fields = (
            'pk',
            'run_date',
            'distance',
            'units',
            'duration',
            'description',
            'run_type',
            'gear',)
        extra_kwargs = {
            'pk': {'read_only': True}}
