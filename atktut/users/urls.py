from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserDetailViewSet, UserCreateViewSet

router = DefaultRouter()
router.register(r'users', UserDetailViewSet)
router.register(r'users', UserCreateViewSet)

user_list = UserViewSet.as_view({
    'get': 'list'
})

register = UserCreateViewSet.as_view({
    'post': 'create'
})

urlpatterns = [
    path(r'users/', user_list, name='user-list'),
    path(r'users/register/', register, name='register-user')
] + router.urls
