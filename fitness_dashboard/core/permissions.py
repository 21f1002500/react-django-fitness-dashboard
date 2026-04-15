from rest_framework.permissions import BasePermission

from accounts.models import Coach
from .models import CoachModuleAccess


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'SUPER_ADMIN'
        )


class IsSuperAdminOrCoach(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role in ('SUPER_ADMIN', 'COACH')
        )


class HasCoachModuleAccess(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role == 'SUPER_ADMIN':
            return True
        if request.user.role != 'COACH':
            return False

        module_code = getattr(view, 'module_code', None)
        if not module_code:
            return False

        try:
            coach = request.user.coach_profile
        except Coach.DoesNotExist:
            return False

        return CoachModuleAccess.objects.filter(
            coach=coach,
            module__code=module_code,
            is_enabled=True,
        ).exists()
