from random import randint

from api.permissions import ModeratorPermission, UserPermission
from api.serializers import (TokenSerializer,
                             UserSerializer)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import (filters, generics, mixins, pagination, permissions,
                            viewsets)
from rest_framework.permissions import AllowAny, IsAdminUser
from reviews.models import Category, Genre, Review, Title
from users.models import Code, User
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer,\
    RegistrationSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

permission_by_role = {
    'user': UserPermission,
    'moderator': ModeratorPermission,
    'admin': AllowAny
}


def permission_class_by_role(request):
    if request.user.is_anonymous:
        return DjangoModelPermissionsOrAnonReadOnly

    role = request.user.role
    if role in permission_by_role:
        return permission_by_role[role]
    elif request.user.is_superuser:
        return IsAdminUser


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username == 'me'
            queryset = User.objects.filter(username=self.request.user.username)

            return queryset

        queryset = User.objects.all()
        return queryset

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class RegistrationViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        confirmation_code = str(randint(1000, 9999))
        send_mail(
            'Confirmation code for registration',
            f'{confirmation_code}',
            'from@example.com',
            [serializer.validated_data['email']],
            fail_silently=False,
        )
        serializer.save(
            role='user',
            confirmation_code=confirmation_code
        )
        #User.objects.create(
        #    username=serializer.validated_data['username'],
        #    email=serializer.validated_data['email'],
        #    role='user',
        #    confirmation_code=confirmation_code
        #)
        #Registration.objects.create(
        #    username=serializer.validated_data['username'],
        #    confirmation_code=confirmation_code
        #)


class APITokenView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            if user.confirmation_code == serializer.validated_data['confirmation_code']:
                return Response(get_tokens_for_user(user),
                                status=status.HTTP_200_OK)
        return Response(
            {'Код введен неверно. Повторите попытку.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes = [ ... ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title=title)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        title = get_object_or_404(Title, pk=title_id)
        review = get_object_or_404(Review, pk=review_id, title=title)
        serializer.save(title=title, review=review, author=self.request.user)

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination
    # permission_classes = [ ... ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class CreateRetrieveDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitlesFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    # pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class GenreViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    # pagination_class = pagination.LimitOffsetPagination
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    # pagination_class = pagination.LimitOffsetPagination
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'

    def get_permissions(self):
        permission_classes = [permission_class_by_role(self.request)]
        return [permission() for permission in permission_classes]
