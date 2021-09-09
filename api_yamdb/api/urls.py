from django.urls import include, path
from rest_framework import routers
from api.views import UserViewSet, RegistrationViewSet


urlpatterns = [
    path('v1/auth/signup', RegistrationViewSet.as_view()),
    #path('v1/auth/token', RegistrationViewSet),
]
