from rest_framework import serializers

from .models import Question, Cat, Log

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class CatSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=True)
    class Meta:
        model = Cat
        fields = ('name', 'url', 'question')

class AnsSerializer(serializers.Serializer):
    qid = serializers.IntegerField()
    ans = serializers.IntegerField()

    def validate_ans(self, value):
        if value not in [0,1,2,3,4]:
            raise serializers.ValidationError("عددی بین 0 تا 4 وارد کنید")
        return value

class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'