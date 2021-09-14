from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only for others.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to edit content.
    Read-only for others
    """
    
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator'
                or request.method in permissions.SAFE_METHODS)


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access content.
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin'
                or request.user.is_superuser)
