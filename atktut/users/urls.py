from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserCreateViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

register = UserCreateViewSet.as_view({
    'post': 'create'
})

urlpatterns = [
    path(r'users/register/', register, name='register-user')
] + router.urls