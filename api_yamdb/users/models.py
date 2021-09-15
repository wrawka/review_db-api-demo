from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def username_validator(name):
    if name == 'me':
        raise ValidationError("Username can't be 'me'")
    else:
        return name


CHOICES = (
    ('user', 'юзер'),
    ('moderator', 'модератор'),
    ('admin', 'админ')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=254
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.TextField(
        'Роль',
        choices=CHOICES,
    )
    confirmation_code = models.PositiveIntegerField(
        'Code',
        blank=True,
        null=True,
    )


class Code(models.Model):
    username = models.TextField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    confirmation_code = models.PositiveIntegerField('Code')
