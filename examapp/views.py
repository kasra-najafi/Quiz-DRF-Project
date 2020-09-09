from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

import datetime

# from .permissions import 

from .models import Question, Cat, Log
from .serializers import QuestionSerializer, CatSerializer, AnsSerializer, LogSerializer

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('cat', 'id')
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Question.objects.all()
        cat = self.request.query_params.get('cat', None)
        dif = self.request.query_params.get('difficulty', None)
        if cat is not None:
            queryset = queryset.filter(cat=cat)
        if dif is not None:
            queryset = queryset.filter(difficulty=dif)
        return queryset


class CatView(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

class LogView(viewsets.ReadOnlyModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer

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
                    Log.objects.create(datetime=datetime.datetime.now(), qid=qid, ans=ans, status='nothing')
                    return Response("شما جوابی به این سوال ندادید")
                elif question.trueans == str(ans):
                    question.correct = F('correct') + 1
                    question.save()
                    question.refresh_from_db()
                    Log.objects.create(datetime=datetime.datetime.now(), qid=qid, ans=ans, status='correct')
                    return Response("شما جواب درست به این سوال دادید")
                else:
                    question.wrong = F('wrong') + 1
                    question.save()
                    question.refresh_from_db()
                    Log.objects.create(datetime=datetime.datetime.now(), qid=qid, ans=ans, status='wrong')
                    return Response("شما جواب اشتباه به این سوال دادید")
            except:
                return Response("چنین سوالی وجود ندارد")
            