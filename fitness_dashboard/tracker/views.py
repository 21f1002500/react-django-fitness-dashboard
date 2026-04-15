from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication  import JWTAuthentication

from rest_framework.exceptions import PermissionDenied

from .models import Tracker
from .serializers import TrackerSerializer
from core.permissions import HasCoachModuleAccess


class TrackerViewSet(viewsets.ModelViewSet):
    queryset = Tracker.objects.select_related('client', 'coach').all()
    serializer_class = TrackerSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasCoachModuleAccess]
    module_code = 'TRACKER'

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
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Exception:
                raise PermissionDenied('Coach profile not found.')
            serializer.save(coach=coach)
        else:
            serializer.save()
