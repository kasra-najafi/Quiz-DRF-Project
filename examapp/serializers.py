from rest_framework import serializers

from .models import Question, Cat, Log, Profile
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields  = ('correct', 'wrong', 'nothing')

        def create(self, validated_data):
            obj = self.Meta.model(**validated_data)
            view = self._context['view']
            request = self._context['request']
            for permission in view.permission_classes:
                if not permission.has_object_permission(self, request, view, obj):
                    raise ValueError('not authorized')
            super(QuestionSerializer, self).create(validated_data)

class CatSerializer(serializers.HyperlinkedModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)
    # question = serializers.StringRelatedField(many=True)
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields  = ('qnumber', 'score')