import random

from django.core.mail import send_mail


def send_mail_code(email: str) -> int:
    """ Отправка письма на email"""

    confirmation_code = random.randint(00000, 99999)
    send_mail(
        'Код подтверждения регистрации',
        'Вы зарегистрированы на YAMDB!'
        f' Ваш код подтвержения: {confirmation_code}',
        'admin@yamdb.com',
        [email],
        fail_silently=False,
    )
    return confirmation_code
