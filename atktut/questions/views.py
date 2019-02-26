from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
import json
from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer

from atktut.course.models import Progress, Lesson
from atktut.course.serializers import ProgressSerializer, LessonSerializer


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
    data = request.data
    unit = data.get('unit')
    course = data.get('course')
    lesson_id = data.get('lesson')
    user = request.user
    progress = None
    next_lesson = None
    query = Lesson.objects.filter(unit_id=unit)
    total_lessons = query.count()

    if not unit or not course or not lesson_id:
        return Response(data={'message': 'invalid request'},
                            status=status.HTTP_400_BAD_REQUEST)

    current_index = list(query.values_list('id', flat=True)).index(int(lesson_id))
    lesson = query[current_index]
    try:
        next_index = list(query.values_list('order', flat=True)).index(query[lesson].order + 1)
        next_lesson = query[next_index]
    except Exception:
        pass

    try:
        progress = Progress.objects.get(owner=user, course=course)
    except Exception:
        pass

    if not progress:
        progress = Progress.objects.create(
            total_lessons=total_lessons,
            unit=unit,
            lesson=lesson.id,
            owner=user,
            course=course,
        )
        progress.completed_lessons.add(lesson)
    else:
        progress.lesson = lesson
        progress.total_lessons = total_lessons
        progress.unit_id = unit
        progress.save
        if not lesson in progress.completed_lessons.all():
            progress.completed_lessons.add(lesson)
    serializer = LessonSerializer(next_lesson)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def answer(request):
    question_id = request.data.get('question')
    answers = request.data.get('answers')

    if not question_id or not answers:
        return Response(data={'message': 'invalid request'},
                            status=status.HTTP_400_BAD_REQUEST)

    question = get_object_or_404(Question.objects.all(), pk=question_id)
    answers_query = Answer.objects.filter(question=question)

    correct = True
    # selected_answers = []
    if not question.question_type == Question.BLANKQUESTION:
        answers = eval(answers)

    if question.question_type == Question.TRUEFALSE or question.question_type == Question.SINGLECHOICE:
        if len(answers) > 1:
            print("invalid legnth is greater")
            correct = False

    if not question.question_type == Question.BLANKQUESTION:
        for ans in answers_query:
            print(ans.id, ans.correct)
            if ans.correct and ans.id not in answers:
                print("invalid answer not in array")
                correct = False

    print(answers)
    if correct:
        return Response(data={'message':'answer correct'})

    return Response(data={'message':'answer incorrect'}, status=status.HTTP_400_BAD_REQUEST)