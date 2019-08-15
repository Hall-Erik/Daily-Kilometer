from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerCanPostOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Read-only methods: GET, HEAD, OPTIONS are fine.
        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only methods: GET, HEAD, OPTIONS are fine
        if request.method in SAFE_METHODS:
            return True

        return request.user == obj.user
