from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer


class UserDetailViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)

class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


# @api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated, ))
# def progress(request):
#     unit_id = request.data.get('unit_id')
#     course_id = request.data.get('course_id')
#     lesson_id = request.data.get('lesson_id')
