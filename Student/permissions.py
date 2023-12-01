from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user has the 'student' role
        return request.user.role == 'student'