from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read-only for others.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and obj.author == request.user))


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to edit content.
    Read-only for others
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.is_moderator)


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to access content.
    """

    def has_permission(self, request, view):
        return (
            (request.user.is_authenticated and request.user.is_admin)
            or request.user.is_superuser)


class IsMeRequest(permissions.BasePermission):
    """
    Custom permission to /api/v1/users/me/ endpoint.
    """

    def has_object_permission(self, request, view, obj):
        if request.method == 'PATCH':
            return (request.user.is_authenticated
                    and request.user.is_admin)
        elif request.method == 'GET':
            return (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_admin))
