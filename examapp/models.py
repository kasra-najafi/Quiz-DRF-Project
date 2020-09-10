from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Cat(models.Model):
    """
    categories
    """    
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

class Question(models.Model):
    """
    questions
    """    
    Difficulty = [
        ('hard', 'hard'),
        ('mid', 'mid'),
        ('easy', 'easy'),
    ]
    content = models.CharField(max_length=1000)
    option1 = models.CharField(max_length=1000)
    option2 = models.CharField(max_length=1000)
    option3 = models.CharField(max_length=1000)
    option4 = models.CharField(max_length=1000)
    trueans = models.CharField(max_length=3)
    cat = models.ForeignKey(Cat, related_name='question', on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=4 ,choices=Difficulty, default='mid')
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.content

class Profile(models.Model):
    """
    Profiles
    """  
    # qnumber means number of question that user answer  
    qnumber = models.IntegerField(default=0)
    score = models.FloatField(max_length=250, default=0)
    user = models.OneToOneField(User, related_name='profile', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.first_name


class Log(models.Model):
    """
    logs
    """    
    Answer_Status = [
        ('correct', 'correct'),
        ('wrong', 'wrong'),
        ('nothing', 'nothing'),
    ]
    datetime = models.DateTimeField()
    qid = models.ForeignKey(Question, related_name='log', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='log', on_delete=models.PROTECT)
    ans = models.IntegerField()
    status = models.CharField(max_length=10, choices=Answer_Status)