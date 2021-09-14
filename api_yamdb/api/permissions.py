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
         return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class IsModerator(permissions.BasePermission):
    """
    Custom permission to only allow moderators to edit content.
    Read-only for others
    """
    
    def has_permission(self, request, view):
        return ( request.method in permissions.SAFE_METHODS
                or request.user.role == 'moderator')


class IsAdmin(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit content.
    Read-only for others
    """

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'admin'
                or request.user.is_superuser)




# class UserPermission(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if ('reviews/' or 'comments/') in request.get_full_path():
#             auth_user = request.user.is_authenticated
#             if (auth_user == request.user.is_authenticated) or\
#                     (request.method in permissions.SAFE_METHODS):
#                 return True
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS\
#             or obj.username == request.user.username


# class ModeratorPermission(UserPermission):

#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS\
#             or obj.author == request.user or obj.author != request.user


# class AnonymousPermission(UserPermission):
#     def has_permission(self, request, view):
#         if ('reviews/' or 'comments/' or 'categories/') in request.get_full_path() and \
#                 (request.method in permissions.SAFE_METHODS):
#             return True
#         else:
#             return False

#     def has_object_permission(self, request, view, obj):
#         return request.method in permissions.SAFE_METHODS
