from rest_framework.permissions import BasePermission

__all__ = ["IsAuthenticated", "IsMaid", "IsSupervisor", "IsSuperuser"]


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_active and request.user.is_authenticated
        )


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_active and request.user.is_superuser
        )


class IsMaid(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_active and request.user.is_maid)


class IsSupervisor(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_active and request.user.is_supervisor
        )
