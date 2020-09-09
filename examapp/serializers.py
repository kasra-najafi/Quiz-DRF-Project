from rest_framework import serializers

from .models import Question, Cat

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class CatSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Cat
        fields = '__all__'