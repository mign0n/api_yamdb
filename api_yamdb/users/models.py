from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_user(value):
    '''Проверка поля username.'''
    if value.lower() == 'me':
        raise ValidationError('Использовать имя <me> запрещено.')

class CustomUser(AbstractUser):

    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('moderator', 'Moderator'),
    )

    username = models.CharField(max_length=150,
            verbose_name='Логин',
            help_text='Укажите логин',
            unique=True,
            validators=[validate_user])

    email = models.EmailField(max_length=254,
            verbose_name='Email address',
            help_text='Укажите email',
            unique=True,
            null=False)

    first_name = models.CharField(max_length=150,
            verbose_name='Имя',
            help_text='Укажите Имя',
            blank=True)

    last_name = models.CharField(max_length=150,
            verbose_name='Фамилия',
            help_text='Укажите Фамилию',
            blank=True)

    bio = models.TextField(max_length=1000,
            verbose_name='Биография',
            help_text='Укажите Биографию',
            blank=True)

    role = models.CharField(max_length=100,
            verbose_name='Роль',
            choices=ROLES,
            default='user',
            help_text='Уровень доступа')

    confirmation_code = models.CharField(max_length=10,
            blank=True,
            verbose_name='Код подтверждения')    


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return self.username

