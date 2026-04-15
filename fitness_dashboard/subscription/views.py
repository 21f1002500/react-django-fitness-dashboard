from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication  import JWTAuthentication


from .models import Subscription
from .serializers import SubscriptionSerializer
from core.permissions import IsSuperAdmin


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.select_related('coach', 'coach__user').all()
    serializer_class = SubscriptionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Exception:
                return queryset.none()
            return queryset.filter(coach=coach)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role != 'SUPER_ADMIN':
            raise PermissionDenied('Only Super Admin can assign subscriptions.')
        serializer.save()
