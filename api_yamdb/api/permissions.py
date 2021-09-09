from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_resource_permission(self, request):
        if ('reviews/' or 'comments/') in request.get_full_path():
            return True
        else:
            return False

    def has_permission(self, request, view):
        safe_method = request.method in permissions.SAFE_METHODS
        auth_user = request.user.is_authenticated
        return safe_method or auth_user

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS\
            or obj.author == request.user


class ModeratorPermission(UserPermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS\
            or obj.author == request.user or obj.author != request.user
