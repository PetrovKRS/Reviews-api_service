from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def validate_me(username):
    if username == 'me':
        raise ValidationError(
            'Использовать имя me запрещено'
        )


validator_username = RegexValidator(
    regex=r'^[\w.@+-]+\Z',
    message='В имени пользователя можно использовать только буквы,'
            ' цифры и символы "@/./+/-/_"!',
)
