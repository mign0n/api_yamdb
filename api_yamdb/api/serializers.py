import re

from django.conf import settings
from rest_framework import serializers

from users.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    
    def validate_username(self, value):
        
        match = re.fullmatch(settings.USERNAME_PATTERN_REGEX, value)
        if not match:
            raise serializers.ValidationError(
                'Имя пользователя некорректно.'
            )
        return value

class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    
    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code', )
