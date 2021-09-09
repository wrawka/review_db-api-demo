from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from reviews.models import Title, Genre, Category


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_fields = ('category', 'genre', 'name', 'year')


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
