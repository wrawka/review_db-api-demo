from django.urls import include, path, re_path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, TitleViewSet, CategoryViewSet,\
    GenreViewSet, UserViewSet, RegistrationViewSet, APITokenView

router = DefaultRouter()
router.register(r'titles', TitleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'users', UserViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/auth/token/', APITokenView.as_view()),
    path('v1/auth/signup/', RegistrationViewSet.as_view()),
    # path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(router.urls)),
]
