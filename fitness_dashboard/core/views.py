from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied                                
from rest_framework_simplejwt.authentication  import JWTAuthentication
from .models import AppConfiguration, Analytics, CoachModuleAccess, Module
from .permissions import HasCoachModuleAccess, IsSuperAdmin
from .serializers import AppConfigurationSerializer, AnalyticsSerializer, CoachModuleAccessSerializer, ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Exception:
                return queryset.none()
            return queryset.filter(
                coachmoduleaccess__coach=coach,
                coachmoduleaccess__is_enabled=True,
            ).distinct()
        return queryset


class CoachModuleAccessViewSet(viewsets.ModelViewSet):
    queryset = CoachModuleAccess.objects.select_related('coach', 'module').all()
    serializer_class = CoachModuleAccessSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]


class AppConfigurationViewSet(viewsets.ModelViewSet):
    queryset = AppConfiguration.objects.all()
    serializer_class = AppConfigurationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]


class AnalyticsViewSet(viewsets.ModelViewSet):
    queryset = Analytics.objects.select_related('client', 'module').all()
    serializer_class = AnalyticsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasCoachModuleAccess]
    module_code = 'ANALYTICS'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Exception:
                return queryset.none()
            return queryset.filter(client__coach=coach)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Exception:
                raise PermissionDenied('Coach profile required.')
            client = serializer.validated_data.get('client')
            if client.coach != coach:
                raise PermissionDenied('Coach can only create analytics for own clients.')
        serializer.save()
