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
    answers = models.CharField(max_length=1000)
    trueans = models.CharField(max_length=3)
    cat = models.ForeignKey(Cat, related_name='question', on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=4 ,choices=Difficulty, default='mid')
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    nothing = models.IntegerField(default=0)

    def __str__(self):
        return self.content