from rest_framework import serializers
from .models import Run, Gear
from users.serializers import UserOnlySerializer


class GearSerializer(serializers.ModelSerializer):
    user = UserOnlySerializer(read_only=True)
    start_miles = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='get_starting_miles',
        read_only=True)
    total_miles = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='get_total_miles',
        read_only=True)

    class Meta:
        model = Gear
        fields = (
            'pk',
            'name',
            'start_miles',
            'start_distance',
            'start_units',
            'total_miles',
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

    def save_gear(self, user, instance, validated_data):
        gear_id = validated_data.pop('gear_id', None)
        if gear_id:
            gear = user.gear_set.get(id=gear_id)
            if gear:
                instance.gear = gear
                instance.save()

    def create(self, validated_data):
        instance = super(RunCreateSerializer, self).create(validated_data)
        user = validated_data['user']
        self.save_gear(user, instance, validated_data)
        return instance

    def update(self, inst, validated_data):
        instance = super(
            RunCreateSerializer, self).update(inst, validated_data)
        user = instance.user
        self.save_gear(user, instance, validated_data)
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
