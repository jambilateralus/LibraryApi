from rest_framework import permissions


class CreatePutDeleteAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' or \
                        request.method == 'DELETE' or \
                        request.method == 'PATCH' or \
                        request.method == 'PUT':
            return request.user.is_superuser
        # if GET request
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST' or \
                        request.method == 'DELETE' or \
                        request.method == 'PATCH' or \
                        request.method == 'PUT':
            return request.user.is_superuser
        # if GET request
        return request.user.is_authenticated


class AllowMemberOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']:
            return request.user.is_authenticated and not request.user.is_superuser
        return False


class AllowAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST', 'DELETE', 'PUT', 'PATCH']:
            return request.user.is_superuser
        return False
