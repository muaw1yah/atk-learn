from rest_framework import routers
from django.urls import path

from .views import QuestionViewSet, AnswerViewSet, progress, answer

router = routers.SimpleRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = [
    path(r'update-progress/', progress, name='update-progress'),
    path(r'answer-question/', answer, name='answer-question'),
] + router.urls
