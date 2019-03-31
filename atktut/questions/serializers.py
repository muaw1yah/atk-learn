from rest_framework import serializers
from .models import Question, Answer

class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        exclude = ('correct',)

    # def __init__(self, *args, **kwargs):
    #     super(AnswerSerializer, self).__init__(*args, **kwargs)
    #     if 'context' in kwargs:
    #         if 'request' in kwargs['context']:
    #             included = set(['content', 'question', 'correct'])
    #             existing = set(self.fields.keys())

    #             for other in existing - included:
    #                 self.fields.pop(other)

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'content', 'question_type', 'hint', 'answers',)
