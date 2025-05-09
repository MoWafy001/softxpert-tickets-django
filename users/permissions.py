from rest_framework.permissions import BasePermission
from .enums import Role

class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ADMIN.value


class IsAgent(BasePermission):
    """
    Allows access only to agent users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.SUPPORT_AGENT.value