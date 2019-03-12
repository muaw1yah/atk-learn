from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from atktut.questions.models import Question
from atktut.questions.serializers import QuestionSerializer
from generic_relations.relations import GenericRelatedField
from .models import Course, Lecture, Lesson, Progress, Unit


class CourseSerializer(serializers.ModelSerializer):
    unit_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'unit_count', 'lesson_count', 'hero_image', 'progress', )

    def get_unit_count(self, obj):
        return obj.units.count()

    def get_lesson_count(self, obj):
        return obj.lessons_course.count()

    def get_progress(self, obj):
        request = self._context.get('request')
        try:
            return ProgressSerializer(obj.progress.get(owner=request.user)).data
        except Exception:
            pass

class UnitSerializer(serializers.ModelSerializer):
    progress = serializers.SerializerMethodField()
    first_lesson = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'description', 'course', 'first_lesson', 'progress', )

    def get_first_lesson(self, obj):
        lessons = obj.lessons.all()
        if len(lessons) > 0:
            return lessons[0].id

    def get_progress(self, obj):
        request = self._context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return ProgressSerializer(obj.progress.get(owner=request.user)).data
            except Exception:
                pass

class LectureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lecture
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    """
    A `Lesson` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """
    unit_object = GenericRelatedField({
        Lecture: LectureSerializer(),
        Question: QuestionSerializer()
    }, read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'order', 'description', 'unit',
                  'content_type', 'course', 'object_id', 'unit_object',)
        read_only_fields = ('unit_object',)

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model',
    )

class UnitDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'description', 'course', 'progress', )

    def get_progress(self, obj):
        request = self._context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return ProgressSerializer(obj.progress.get(owner=request.user)).data
            except Exception:
                pass

class CourseDetailSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'units', 'hero_image', 'progress',)

    def get_progress(self, obj):
        request = self._context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return ProgressSerializer(obj.progress.get(owner=request.user)).data
            except Exception:
                pass

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        exclude = ('created', 'updated', 'owner', )

class ProgressDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)

    class Meta:
        model = Progress
        read_only_fields = ('course',)
        exclude = ('created', 'updated', 'owner', )
