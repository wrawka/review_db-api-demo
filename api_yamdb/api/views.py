from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (CharFilter, DjangoFilterBackend,
                                           FilterSet)
from rest_framework import (filters, generics, mixins, pagination, status,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from api.permissions import IsAdmin, IsAuthorOrReadOnly, IsModerator, ReadOnly
from api.serializers import UserSerializer, UserSerializerWithoutRole

from . import serializers


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
    }


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdmin]

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        serializer = UserSerializerWithoutRole(user, data=request.data,
                                               partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RegistrationViewSet(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer
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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK,
                        headers=headers)


class APITokenView(APIView):
    http_method_names = ['post']
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username']
            )
            code = serializer.validated_data['confirmation_code']
            if user.confirmation_code == code:
                return Response(get_tokens_for_user(user),
                                status=status.HTTP_200_OK)
            elif user.is_superuser:
                return Response(get_tokens_for_user(user),
                                status=status.HTTP_200_OK)
        return Response(
            {'Код введен неверно. Повторите попытку.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnly | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAuthorOrReadOnly | IsModerator]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(title=title, author=self.request.user)


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
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAdmin | ReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter


class GenreViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    pagination_class = pagination.LimitOffsetPagination
    permission_classes = [IsAdmin | ReadOnly]
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'
