from rest_framework import serializers

from .models import AppConfiguration, Analytics, CoachModuleAccess, Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name', 'code']
        read_only_fields = ['id']


class CoachModuleAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachModuleAccess
        fields = ['id', 'coach', 'module', 'is_enabled']
        read_only_fields = ['id']


class AppConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfiguration
        fields = ['id', 'key', 'value', 'description', 'is_active', 'updated_at']
        read_only_fields = ['id', 'updated_at']


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = ['id', 'client', 'module', 'data', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']
