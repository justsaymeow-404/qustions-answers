from rest_framework import serializers

from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
    question_id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(source='questions.text', read_only=True)
    user_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question_id', 'question_text', 'user_id', 'text','created_at')
        read_only_fields = ('id', 'question_id', 'created_at')


class AnswerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('text',)
    

class QuestionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'created_at')


class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'created_at', 'answers')


class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text', 'id', 'created_at')
