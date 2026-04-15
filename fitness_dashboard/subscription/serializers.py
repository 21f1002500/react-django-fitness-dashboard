from rest_framework import serializers

from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'coach', 'plan_name', 'start_date', 'end_date', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']
