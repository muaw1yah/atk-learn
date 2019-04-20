from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .models import Answer, Question
from .serializers import AnswerSerializer, QuestionSerializer

from atktut.course.models import Progress, Lesson, Unit
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
    unit_id = request.data.get('unit_id')
    course_id = request.data.get('course_id')
    lesson_id = request.data.get('lesson_id')

    if not unit_id or not course_id or not lesson_id:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)

    progress = None
    query = Lesson.objects.filter(unit_id=unit_id).order_by('order')
    next_lesson = get_next_lesson(request.user, course_id, unit_id, lesson_id, query)

    try:
        progress = Progress.objects.get(owner=request.user, course_id=course_id)
    except Exception:
        pass

    if not progress:
        progress = Progress.objects.create(
            total_lessons=query.count(),
            unit_id=unit_id,
            lesson_id=lesson_id,
            owner=request.user,
            course_id=course_id,
        )
        progress.completed_lessons.add(lesson_id)
    else:
        lesson = query[list(query.values_list('id', flat=True)).index(int(lesson_id))]
        progress.lesson_id = lesson_id
        progress.total_lessons = query.count()
        progress.unit_id = unit_id
        progress.save()
        if lesson not in progress.completed_lessons.all():
            progress.completed_lessons.add(lesson)

    # Update Completed unit
    lessons_comp = 0
    completed_lessons = progress.completed_lessons.all()
    for lesson in query:
        if lesson in completed_lessons:
            lessons_comp += 1
    if query.count() == lessons_comp:
        progress.completed_units.add(unit_id)

    serializer = LessonSerializer(next_lesson)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def complete_unit(request):
    progress_id = request.data.get('progress_id')
    unit_id = request.data.get('unit_id')
    user = request.user

    if not progress_id or not unit_id:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)

    progress = get_object_or_404(Progress.objects.all(), pk=progress_id)
    if progress.owner != user:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)
    progress.completed_units.add(unit_id)
    progress.save()

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated, ))
def answer(request):
    course_id = request.data.get('course_id')
    question_id = request.data.get('question_id')
    answers = request.data.get('answer')
    unit_id = request.data.get('unit_id')
    lesson_id = request.data.get('lesson_id')

    if not question_id or not answers:
        return Response(data={'message': 'invalid request'},
                        status=status.HTTP_400_BAD_REQUEST)

    question = get_object_or_404(Question.objects.all(), pk=question_id)
    answers_query = Answer.objects.filter(question=question).filter(correct=True)

    correct = True
    if not question.question_type == Question.BLANKQUESTION:
        answers = eval(answers)
        for ans in answers_query:
            if ans.id not in answers:
                correct = False

    if question.question_type == Question.TRUEFALSE or question.question_type == Question.SINGLECHOICE:
        if len(answers) > 1:
            correct = False

    if question.question_type == Question.MULTICHOICE and len(answers_query) != len(answers):
        correct = False

    if correct:
        next_lesson = get_next_lesson(request.user, course_id, unit_id, lesson_id)
        serializer = LessonSerializer(next_lesson)
        return Response(serializer.data)

    return Response(data={'message': 'answer incorrect'}, status=status.HTTP_400_BAD_REQUEST)


def get_next_lesson(user, course_id, unit_id, lesson_id, query=None):
    if not query:
        query = Lesson.objects.filter(unit_id=unit_id).order_by('order')
    lesson = query[list(query.values_list('id', flat=True)).index(int(lesson_id))]

    progress = None
    try:
        progress = Progress.objects.get(owner=user, course_id=course_id)
    except Exception:
        pass

    if not progress:
        progress = Progress.objects.create(
            total_lessons=query.count(),
            unit_id=unit_id,
            lesson_id=lesson_id,
            owner=user,
            course_id=course_id,
        )
        progress.completed_lessons.add(lesson_id)
    else:
        progress.lesson_id = lesson_id
        progress.total_lessons = query.count()
        progress.unit_id = unit_id
        progress.save()
        if lesson not in progress.completed_lessons.all():
            progress.completed_lessons.add(lesson)
    try:
        next_lesson = query[list(query.values_list('order', flat=True)).index(int(lesson.order) + 1)]
        if not next_lesson:
            unit_query = Unit.objects.filter(course_id=course_id).order_by('order')
            unit = unit_query[list(unit_query.values_list('id', flat=True)).index(int(unit_id))]
            next_unit = unit_query[list(unit_query.values_list('order',
                                                               flat=True)).index(int(unit.order) + 1)]

            if next_unit:
                query = Lesson.objects.filter(unit_id=next_unit.id).order_by('order')
                return query[0]
            else:
                return None
        else:
            return next_lesson
    except Exception:
        return None
