from rest_framework import serializers

from .models import Tracker


class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tracker
        fields = ['id', 'client', 'coach', 'data', 'date', 'created_at']
        read_only_fields = ['id', 'coach', 'created_at']
