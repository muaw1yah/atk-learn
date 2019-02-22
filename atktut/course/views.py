from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from atktut.questions.models import Question, Answer
from atktut.questions.serializers import QuestionSerializer

from .models import Course, Lecture, Lesson, Unit
from .serializers import (CourseDetailSerializer, CourseSerializer,
                          LectureSerializer, LessonSerializer,
                          UnitDetailSerializer, UnitSerializer)


class LectureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Lecture.objects.all()
    serializer_class = LectureSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CourseDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    permission_classes = (permissions.IsAuthenticated,)

class UnitDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitDetailSerializer
    permission_classes = (permissions.IsAuthenticated,)

class LessonViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def create(self, request):
        data = request.data
        # mutable = data._mutable
        # data._mutable = True        
        if data.get('content_type') == 'question':
            serializer = QuestionSerializer(data=data)
            if serializer.is_valid():
                obj = Question.objects.create(**serializer.validated_data)
                data['object_id'] = obj.pk
                size = int(data.get('answers_size'))
                if size and size > 0:
                    answers_get = lambda *keys: data['answers' + ''.join(['[%s]' % key for key in keys])]
                    answers = data['answers']
                    for i in range(size):
                        # content = answers_get(str(i), 'content')
                        # correct = answers_get(str(i), 'correct')
                        content = answers[i].get('content')
                        correct = bool(answers[i].get('correct'))
                        Answer.objects.create(
                            content=content,
                            correct=correct,
                            question=obj
                        )
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        elif data.get('content_type') == 'lecture':
            serializer = LectureSerializer(data=data)
            if serializer.is_valid():
                obj = Lecture.objects.create(**serializer.validated_data)
                data['object_id'] = obj.pk
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message':'invalid content_type %s' % data.get('content_type')}, status=status.HTTP_400_BAD_REQUEST)
        
        # data._mutable = mutable
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            obj = Lesson.objects.create(**serializer.validated_data)
            return Response(LessonSerializer(obj).data, status=status.HTTP_201_CREATED)

        return Response(data={'message':'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
