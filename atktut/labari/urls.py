from django.urls import path
from .views import LabariViewSet

labari_list = LabariViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

labari_detail = LabariViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path(r'labari/', labari_list, name='labari-list'),
    path(r'labari/<int:pk>/', labari_detail, name='labari-detail'),
]
