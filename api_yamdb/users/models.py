from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.response import Response
from rest_framework import status


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
    confirmation_code = models.PositiveIntegerField(
        'Code',
        blank=True,
        null=True,
    )

    def clean(self):
        if self.username == 'me':
            Response(
                {'Пожалуйста, выберите другой username.'},
                status=status.HTTP_400_BAD_REQUEST
            )


#class Registration(models.Model):
#    username = models.TextField(
#        unique=True,
#        blank=False,
#        null=False,
#        max_length=150
#    )
#    email = models.EmailField('Email', unique=True, max_length=254)
#    confirmation_code = models.PositiveIntegerField('Code')


class Code(models.Model):
    username = models.TextField(
        unique=True,
        blank=False,
        null=False,
        max_length=150
    )
    confirmation_code = models.PositiveIntegerField('Code')
