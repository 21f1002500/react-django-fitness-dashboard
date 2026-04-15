from rest_framework import serializers

from .models import DietPlan


class DietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietPlan
        fields = ['id', 'client', 'coach', 'title', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'coach', 'created_at', 'updated_at']
