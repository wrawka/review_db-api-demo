from rest_framework import serializers
from users.models import User, Registration, JWTToken


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email',)
        model = Registration


class SendConfirCodeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'confirmation_code',)
        model = JWTToken
