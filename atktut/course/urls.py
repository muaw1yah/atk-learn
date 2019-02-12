from django.urls import include, path
from rest_framework import routers, renderers

from .views import CourseViewSet, UnitViewSet, LessonViewSet, UnitDetailViewSet, CourseDetailViewSet

router = routers.SimpleRouter()
router.register(r'lessons', LessonViewSet)

course_list = CourseViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

course_detail = CourseDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

unit_list = UnitViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

unit_detail = UnitDetailViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(r'course/', course_list, name='course-list'),
    path(r'course/<int:pk>/', course_detail, name='course-detail'),
    path(r'units/', unit_list, name='unit-list'),
    path(r'units/<int:pk>/', unit_detail, name='unit-detail'),
] + router.urls