from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка прав доступа для администратора."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role == 'admin'
            or user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.role == 'admin'
            or user.is_superuser
        )


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == 'admin'
        )

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == 'admin'
        )


class IsModerator(permissions.BasePermission):
    """Проверка прав доступа для модератора."""

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (
            user.is_authenticated and user.role == 'moderator'
            and (obj.__class__.__name__ == 'Review'
                 or obj.__class__.__name__ == 'Comment')
        )


class MePermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только текущему юзеру."""

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.username == obj.username
