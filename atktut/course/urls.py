from django.urls import include, path
from rest_framework import routers, renderers

from .views import CourseViewSet, UnitViewSet, LessonViewSet

router = routers.SimpleRouter()
router.register(r'course', CourseViewSet)
router.register(r'units', UnitViewSet)
router.register(r'lessons', LessonViewSet)

# course_list = CourseViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })

# course_detail = CourseViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

# urlpatterns = [
#     path('course/', course_list, name='course-list'),
#     path('course/<int:pk>/', course_detail, name='course-detail'),
# ] + router.urls

urlpatterns = router.urls
