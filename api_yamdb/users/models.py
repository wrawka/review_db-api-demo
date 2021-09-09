from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )
    role = models.TextField(
        'Роль',
        blank=True,
        null=True,
    )


class Registration(models.Model):
    username = models.TextField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    email = models.EmailField('Email', unique=True, max_length=254)
    confirmation_code = models.PositiveIntegerField('Code')


class JWTToken(models.Model):
    username = models.TextField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    confirmation_code = models.PositiveIntegerField('Code')
