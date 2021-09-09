from rest_framework import viewsets
from users.models import User, Registration, JWTToken
from api.serializers import UserSerializer, RegistrationSerializer,\
    SendConfirCodeSerializer
from random import randint
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from api.permissions import UserPermission, ModeratorPermission


permission_classes_by_role = {
    'user': UserPermission,
    'moderator': ModeratorPermission,
    'admin': AllowAny
}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class RegistrationViewSet(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        confirmation_code = randint(1000, 9999)

        serializer.save(
            confirmation_code=confirmation_code
        )


class SendConfirCodeViewSet(generics.ListCreateAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = SendConfirCodeSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        User.objects.create(
            username=self.request.user.username,
            role='user'
        )
        serializer.save()



