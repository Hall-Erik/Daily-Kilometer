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


class RunCreateSerializer(serializers.ModelSerializer):
    gear_id = serializers.IntegerField(required=False, allow_null=True)
    user = UserOnlySerializer(read_only=True)
    get_duration = serializers.CharField(read_only=True)
    get_pace = serializers.CharField(read_only=True)

    def create(self, validated_data):
        instance = super(RunCreateSerializer, self).create(validated_data)
        gear_id = validated_data.pop('gear_id', None)
        user = validated_data['user']
        if gear_id:
            gear = user.gear_set.get(id=gear_id)
            if gear:
                instance.gear = gear
                instance.save()
        return instance

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
            'gear_id',
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
