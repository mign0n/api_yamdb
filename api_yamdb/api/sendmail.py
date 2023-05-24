from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import QuerySet


def send_mail_code(user: QuerySet) -> int:
    """Отправка письма на email"""

    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Код подтверждения регистрации',
        'Вы зарегистрированы на YAMDB!'
        f' Ваш код подтвержения: {confirmation_code}',
        settings.ADMIN_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return confirmation_code
