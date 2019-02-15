from django.urls import include, path
from rest_framework import routers, renderers

from .views import QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = router.urls