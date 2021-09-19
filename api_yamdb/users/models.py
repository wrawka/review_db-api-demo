from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models

USER_ROLE = ('user', 'юзер')
MODERATOR_ROLE = ('moderator', 'модератор')
ADMIN_ROLE = ('admin', 'админ')


def username_validator(name):
    if name == 'me':
        raise ValidationError("Username can't be 'me'")


CHOICES = (
    USER_ROLE,
    MODERATOR_ROLE,
    ADMIN_ROLE
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
    confirmation_code = models.TextField(
        'Code',
        blank=True,
        null=True,
    )

    @property
    def is_moderator(self):
        return self.role == MODERATOR_ROLE[0]

    @property
    def is_admin(self):
        return self.role == ADMIN_ROLE[0]


class Code(models.Model):
    username = models.TextField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    confirmation_code = models.TextField('Code')
