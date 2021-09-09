from rest_framework import filters, viewsets, mixins
from django_filters.rest_framework import (DjangoFilterBackend,
                                           FilterSet, CharFilter)

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from reviews.models import Title, Genre, Category


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
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = TitlesFilter


class GenreViewSet(CreateRetrieveDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'


class CategoryViewSet(CreateRetrieveDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'
    lookup_value_regex = '[^/]+'

