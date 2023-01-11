from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()
routers.register('auth', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(routers.urls)),
    path('signup', RegisterView.as_view()),
    path('auth', AuthViewSet.as_view({'post':'login', 'get':'logout'})),
]