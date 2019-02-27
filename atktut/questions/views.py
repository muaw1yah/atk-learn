from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer

from atktut.course.models import Progress, Lesson
from atktut.course.serializers import LessonSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (permissions.IsAdminUser, )

class AnswerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows courses to be viewed or edited.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (permissions.IsAdminUser, )

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def progress(request):
    unit = request.data.get('unit')
    course = request.data.get('course')
    lesson_id = request.data.get('lesson')
    user = request.user
    progress = None
    next_lesson = None
    query = Lesson.objects.filter(unit_id=unit).order_by('order')
    total_lessons = query.count()

    if not unit or not course or not lesson_id:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)

    current_index = list(query.values_list('id', flat=True)).index(int(lesson_id))
    lesson = query[current_index]
    try:
        next_index = list(query.values_list('order', flat=True)).index(int(lesson.order) + 1)
        next_lesson = query[next_index]
    except Exception:
        pass

    try:
        progress = Progress.objects.get(owner=user, course_id=course)
    except Exception:
        pass

    if not progress:
        progress = Progress.objects.create(
            total_lessons=total_lessons,
            unit_id=unit,
            lesson_id=lesson.id,
            owner=user,
            course_id=course,
        )
        progress.completed_lessons.add(lesson)
    else:
        progress.lesson = lesson
        progress.total_lessons = total_lessons
        progress.unit_id = unit
        progress.save
        if lesson not in progress.completed_lessons.all():
            progress.completed_lessons.add(lesson)
    serializer = LessonSerializer(next_lesson)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def answer(request):
    question_id = request.data.get('question_id')
    answers = request.data.get('answer')
    unit_id = request.data.get('unit_id')
    lesson_id = request.data.get('lesson_id')

    if not question_id or not answers:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)

    question = get_object_or_404(Question.objects.all(), pk=question_id)
    answers_query = Answer.objects.filter(question=question)

    correct = True
    if not question.question_type == Question.BLANKQUESTION:
        answers = eval(answers)
        for ans in answers_query:
            if ans.correct and ans.id not in answers:
                correct = False

    if question.question_type == Question.TRUEFALSE or question.question_type == Question.SINGLECHOICE:
        if len(answers) > 1:
            correct = False

    if correct:
        next_lesson = None
        query = Lesson.objects.filter(unit_id=unit_id).order_by('order')
        lesson = query[list(query.values_list('id', flat=True)).index(int(lesson_id))]
        try:
            next_lesson = query[list(query.values_list('order', flat=True)).index(int(lesson.order) + 1)]
        except Exception:
            pass
        serializer = LessonSerializer(next_lesson)
        return Response(serializer.data)

    return Response(data={'message': 'answer incorrect'}, status=status.HTTP_400_BAD_REQUEST)
