from rest_framework import serializers

from .models import FitnessPlan


class FitnessPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessPlan
        fields = ['id', 'client', 'coach', 'title', 'exercise', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'coach', 'created_at', 'updated_at']
