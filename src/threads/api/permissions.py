from rest_framework import permissions

class DeleteOwnThreadComment(permissions.BasePermission):
    """Allow admin_student and user to delete their own thread or comment"""
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser or obj.author == request.user
