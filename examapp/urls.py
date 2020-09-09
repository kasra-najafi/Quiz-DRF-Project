from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('question', views.QuestionView)
router.register('category', views.CatView)


urlpatterns = [
    path('', include(router.urls))
]