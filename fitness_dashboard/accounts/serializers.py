from rest_framework import serializers

from .models import User, Coach, Client


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_password(User.objects.make_random_password())
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = ['id', 'user', 'is_active']
        read_only_fields = ['id']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'user', 'coach', 'name', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']
