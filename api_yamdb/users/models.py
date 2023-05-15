from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('moderator', 'Moderator'),
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        null=True,
    )

    role = models.CharField(
        verbose_name='Уровень доступа',
        max_length=20,
        choices=ROLES,
        default='user',
    )

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username
