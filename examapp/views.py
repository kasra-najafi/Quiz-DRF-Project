from django.shortcuts import render
from django.db.models import F
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

import datetime

from .permissions import IsSuperOrReadOnly, IsSuperOrProfileOwner

from .models import Question, Cat, Log, Profile
from .serializers import (QuestionSerializer, CatSerializer, AnsSerializer, 
                        LogSerializer, ProfileSerializer)

class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.filter().order_by('cat', 'id')
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsSuperOrReadOnly]

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.action == 'create':
    #         permission_classes = [IsSuperOrReadOnly]
    #     return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user.is_superuser:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)   
        else:
            return Response("با کاربر ادمین وارد شوید")

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

    def get_queryset(self):
        """
        Optionally restricts the returned questions in order by category and id,
        by filtering against a `category` or a specific 'difficulty' query parameter in the URL.
        """
        if self.request.user.is_superuser:
            queryset = Question.objects.all().order_by('cat', 'id')
        else:
            queryset = Question.objects.filter(is_show=True).order_by('cat', 'id')
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


# def calculating(question, s):
#     question.nothing = F(s) + 1
#     question.save()
#     question.refresh_from_db()
#     pass

class AnsView(APIView):
    serializer_class = AnsSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            profile = request.user.profile
            qid = serializer.validated_data.get("qid")
            ans = serializer.validated_data.get("ans")
            question = Question.objects.get(id=qid)
            profile.qnumber = F('qnumber') + 1
            profile.save()
            profile.refresh_from_db()
            
            try:
                if ans == 0:
                    s = 'nothing'
                    question.nothing = F('nothing') + 1
                    question.save()
                    question.refresh_from_db()
                    Log.objects.create(datetime=datetime.datetime.now(), qid=question, ans=ans,
                                                            status='nothing', profile=profile)
                    return Response("شما جوابی به این سوال ندادید")
                elif question.trueans == str(ans):
                    s = 'correct'
                    question.correct = F('correct') + 1
                    question.save()
                    question.refresh_from_db()
                    profile.score = F('score') + 3
                    profile.save()
                    profile.refresh_from_db()
                    Log.objects.create(datetime=datetime.datetime.now(), qid=question, ans=ans,
                                                            status='correct', profile=profile)
                    return Response("شما جواب درست به این سوال دادید")
                else:
                    s = 'wrong'
                    question.wrong = F('wrong') + 1
                    question.save()
                    question.refresh_from_db()
                    profile.score = F('score') - 1
                    profile.save()
                    profile.refresh_from_db()
                    Log.objects.create(datetime=datetime.datetime.now(), qid=question, ans=ans, 
                                                            status=s, profile=profile)
                    return Response("شما جواب اشتباه به این سوال دادید")


            except:
                return Response("چنین سوالی وجود ندارد")
            


class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated, IsSuperOrProfileOwner]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Profile.objects.all()
        else:
            return Profile.objects.filter(user = self.request.user)
    