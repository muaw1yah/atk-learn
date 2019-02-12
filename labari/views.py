from .models import Labari
from rest_framework import viewsets, permissions
from .serializers import LabariSerializer
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from commons.permissions import IsUserOrReadOnly


class LabariViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Labari.objects.all()
    serializer_class = LabariSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsUserOrReadOnly, )
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)