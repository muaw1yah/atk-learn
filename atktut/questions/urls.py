from rest_framework import routers

from .views import QuestionViewSet, AnswerViewSet

router = routers.SimpleRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = router.urls
