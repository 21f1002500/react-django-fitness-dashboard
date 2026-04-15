from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication  import JWTAuthentication
from rest_framework.exceptions import PermissionDenied

from .models import Coach, Client, User
from .serializers import ClientSerializer, CoachSerializer, UserSerializer
from core.permissions import IsSuperAdmin, IsSuperAdminOrCoach


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'me':
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsSuperAdmin()]

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.select_related('user').all()
    serializer_class = CoachSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.select_related('user', 'coach__user').all()
    serializer_class = ClientSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdminOrCoach]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Coach.DoesNotExist:
                return queryset.none()
            return queryset.filter(coach=coach)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role == 'COACH':
            try:
                coach = self.request.user.coach_profile
            except Coach.DoesNotExist:
                raise PermissionDenied('Coach profile not found.')
            serializer.save(coach=coach)
        else:
            serializer.save()
