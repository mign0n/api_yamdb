from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.request import Request


class IsAdmin(permissions.BasePermission):
    """Проверка прав доступа для администратора."""

    def has_permission(self, request: Request, view: QuerySet) -> bool:
        user = request.user
        return user.is_authenticated and user.is_admin or user.is_superuser

    def has_object_permission(
        self,
        request: Request,
        view: QuerySet,
        obj: QuerySet,
    ) -> bool:
        user = request.user
        return user.is_authenticated and user.is_admin or user.is_superuser


class AdminOrReadOnly(permissions.BasePermission):
    """Полный доступ предоставляется администратору,
    остальным - только для чтения."""

    def has_permission(self, request: Request, view: QuerySet) -> bool:
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated
            and request.user.is_admin
            or request.user.is_superuser
        )


class IsModerator(permissions.BasePermission):
    """Проверка прав доступа для модератора."""

    def has_permission(self, request: Request, view: QuerySet) -> bool:
        user = request.user
        return user.is_authenticated and user.is_moderator

    def has_object_permission(
        self,
        request: Request,
        view: QuerySet,
        obj: QuerySet,
    ) -> bool:
        user = request.user
        return (
            user.is_authenticated
            and user.is_moderator
            and (
                obj.__class__.__name__ == 'Review'
                or obj.__class__.__name__ == 'Comment'
            )
        )


class MePermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только текущему юзеру."""

    def has_permission(self, request: Request, view: QuerySet) -> bool:
        user = request.user
        return user.is_authenticated

    def has_object_permission(
        self,
        request: Request,
        view: QuerySet,
        obj: QuerySet,
    ) -> bool:
        user = request.user
        return user.username == obj.username
