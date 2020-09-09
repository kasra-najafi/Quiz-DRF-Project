from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from .permissions import 

from .models import Question, Cat
from .serializers import QuestionSerializer, CatSerializer, AnsSerializer

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('cat', 'id')
    serializer_class = QuestionSerializer


class CatView(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class AnsView(APIView):
    serializer_class = AnsSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            qid = serializer.validated_data.get("qid")
            ans = serializer.validated_data.get("ans")
            question = Question.objects.get(id=qid)
            try:
                if ans == 0:
                    question.nothing = F('nothing') + 1
                    question.save()
                    question.refresh_from_db()
                    return Response("شما جوابی به این سوال ندادید")
                elif question.trueans == ans:
                    question.correct = F('correct') + 1
                    question.save()
                    question.refresh_from_db()
                    return Response("شما جواب درست به این سوال دادید")
                else:
                    question.wrong = F('wrong') + 1
                    question.save()
                    question.refresh_from_db()
                    return Response("شما جواب اشتباه به این سوال دادید")
            except:
                return Response("چنین سوالی وجود ندارد")