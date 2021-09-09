from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CategoryViewSet, GenreViewSet

router = routers.DefaultRouter()
router.register(r'api/v1/titles', TitleViewSet)
router.register(r'api/v1/categories', CategoryViewSet)
router.register(r'api/v1/genres', GenreViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
