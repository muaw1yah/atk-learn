from .models import Question, Answer
from rest_framework import viewsets, permissions
from .serializers import QuestionSerializer, AnswerSerializer

class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser, )

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAdminUser, )

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)
