from rest_framework import serializers
from .models import Run


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = (
            'pk',
            'run_date',
            'distance',
            'units',
            'duration',
            'description',
            'run_type',)
        extra_kwargs = {
            'pk': {'read_only': True}}
