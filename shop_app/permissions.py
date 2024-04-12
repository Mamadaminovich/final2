from rest_framework.permissions import IsAuthenticatedOrReadOnly

class IsAuthenticatedAndAdminOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True
        return bool(request.user and request.user.is_staff)