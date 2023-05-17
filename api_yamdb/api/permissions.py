from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """Проверка прав доступа для комментариев."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, post):

        return (
            request.method in permissions.SAFE_METHODS
            or post.author == request.user
        )


class IsOwnerFollowPermission(permissions.BasePermission):
    """Проверка прав доступа для подписок."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.following == request.user
