from rest_framework.permissions import BasePermission

class IsProjectsMember(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

class UserPermissionObj(BasePermission):
    """
    Owners of the object or admins can do anything.
    Everyone else can do nothing.
    """
    def has_object_permission(self, request, view, obj):
        if obj.project_contributor == request.user:
            return True
        return obj == request.user

