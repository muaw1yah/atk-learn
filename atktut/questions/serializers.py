from rest_framework import serializers
from .models import Question, Answer
from drf_writable_nested import WritableNestedModelSerializer

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id', 'content', 'correct', 'question')

    # def __init__(self, *args, **kwargs):
    #     super(AnswerSerializer, self).__init__(*args, **kwargs)
    #     if 'context' in kwargs:
    #         if 'request' in kwargs['context']:
    #             included = set(['content', 'question', 'correct'])
    #             existing = set(self.fields.keys())

    #             for other in existing - included:
    #                 self.fields.pop(other)

class QuestionSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'question_type', 'hint', 'answers',)
