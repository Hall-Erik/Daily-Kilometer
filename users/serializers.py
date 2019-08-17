from rest_framework import serializers
from rest_auth.serializers import UserDetailsSerializer
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.CharField(read_only=True)
    latest_shoe_miles = serializers.DecimalField(
        source='get_latest_shoe_miles', read_only=True,
        max_digits=7, decimal_places=2)
    week_miles = serializers.DecimalField(
        source='get_week_miles', read_only=True,
        max_digits=5, decimal_places=2)
    total_miles = serializers.DecimalField(
        source='get_total_miles', read_only=True,
        max_digits=7, decimal_places=2)

    class Meta:
        model = Profile
        fields = (
            'pk',
            'location',
            'gravatar_url',
            'latest_shoe_miles',
            'week_miles',
            'total_miles',)


class UserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'profile',)
        extra_kwargs = {
            'pk': {'read_only': True},
            'email': {'read_only': True}}


class UserOnlySerializer(UserDetailsSerializer):
    gravatar_url = serializers.CharField(
        source='profile.gravatar_url', read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'gravatar_url',)
        extra_kwargs = {
            'pk': {'read_only': True},
            'email': {'read_only': True}}
