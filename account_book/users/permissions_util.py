from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.writer.pk == request.user.pk


class IsLoginOrLogout(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'POST':
            return bool(request.user and request.user.is_authenticated)
        else:
            return True
