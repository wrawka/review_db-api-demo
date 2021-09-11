from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif ('reviews/' or 'comments/') in request.get_full_path():
            auth_user = request.user.is_authenticated
            return auth_user
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS\
            or obj.author == request.user


class ModeratorPermission(UserPermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS\
            or obj.author == request.user or obj.author != request.user
