from random import randint
from rest_framework import filters, mixins, pagination, permissions, viewsets, generics
from rest_framework.permissions import AllowAny, IsAdminUser

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import (DjangoFilterBackend,
                                           FilterSet, CharFilter)
from reviews.models import Review, Title, Genre, Category
from users.models import User, Registration, JWTToken
from .permissions import UserPermission, ModeratorPermission

from . import serializers

# TODO: поправить импорты!

permission_classes_by_role = {
    'user': UserPermission,
    'moderator': ModeratorPermission,
    'admin': AllowAny
}


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    lookup_field = 'username'


class RegistrationViewSet(generics.ListCreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = serializers.RegistrationSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        confirmation_code = randint(1000, 9999)

        serializer.save(
            confirmation_code=confirmation_code
        )


class SendConfirCodeViewSet(generics.ListCreateAPIView):
    queryset = JWTToken.objects.all()
    serializer_class = serializers.SendConfirCodeSerializer
    http_method_names = ['post']

    def perform_create(self, serializer):
        User.objects.create(
            username=self.request.user.username,
            role='user'
        )
        serializer.save()


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


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = serializers.TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = TitlesFilter

    def retrieve(self, request, *args, **kwargs):
        #Расчет рейтинга тайтла про GET запросе


class GenreViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'
