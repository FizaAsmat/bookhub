from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'profile') and request.user.profile.role == 'admin'

class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user,'profile') and request.user.profile.role == 'librarian'