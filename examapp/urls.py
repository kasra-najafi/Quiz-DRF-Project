from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register('question', views.QuestionView)
router.register('category', views.CatView)
# router.register('answer', views.AnsView)


urlpatterns = [
    path('', include(router.urls)),
    path('answer', views.AnsView.as_view()),
]