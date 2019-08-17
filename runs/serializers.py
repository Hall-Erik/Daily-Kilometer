from rest_framework import serializers
from .models import Run, Gear
from users.serializers import UserOnlySerializer


class GearSerializer(serializers.ModelSerializer):
    user = UserOnlySerializer(read_only=True)

    class Meta:
        model = Gear
        fields = (
            'pk',
            'name',
            'start_distance',
            'start_units',
            'date_added',
            'date_retired',
            'user',)
        extra_kwargs = {
            'pk': {'read_only': True}}


class RunSerializer(serializers.ModelSerializer):
    gear = GearSerializer(read_only=True)
    user = UserOnlySerializer(read_only=True)
    get_duration = serializers.CharField(read_only=True)
    get_pace = serializers.CharField(read_only=True)

    class Meta:
        model = Run
        fields = (
            'pk',
            'run_date',
            'distance',
            'units',
            'duration',
            'get_duration',
            'get_pace',
            'description',
            'run_type',
            'gear',
            'user',)
        extra_kwargs = {
            'pk': {'read_only': True}}
