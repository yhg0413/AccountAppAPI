from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ArticleAPI.as_view()),
    path('<int:pk>', ArticleDetailAPI.as_view()),
    path('action/<int:pk>', ActionViewSet.as_view(actions={'post':'copy','get':'shot_url'})),
    path('short/<str:new_link>', origin_redirect)
]