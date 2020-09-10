from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('question', views.QuestionView)
router.register('category', views.CatView)
router.register('log', views.LogView)
router.register('profile', views.ProfileView)


urlpatterns = [
    path('', include(router.urls)),
    path('answer', views.AnsView.as_view()),
]