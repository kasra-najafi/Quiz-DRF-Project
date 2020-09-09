from django.shortcuts import render

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from .permissions import 

from .models import Question, Cat
from .serializers import QuestionSerializer, CatSerializer

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CatView(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer