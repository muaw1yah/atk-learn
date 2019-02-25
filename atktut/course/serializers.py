from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from atktut.questions.models import Question
from atktut.questions.serializers import QuestionSerializer
from generic_relations.relations import GenericRelatedField
from .models import Course, Lecture, Lesson, Progress, Unit

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        exclude = ('created', 'updated', 'owner', )


class CourseSerializer(serializers.ModelSerializer):
    unit_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'unit_count', 'progress', )

    def get_unit_count(self, obj):
        return obj.units.count()

    def get_progress(self, obj):
        request = self._context.get('request')
        try:
            return ProgressSerializer(obj.progress.get(owner=request.user)).data
        except Exception:
            pass

class UnitSerializer(serializers.ModelSerializer):
    unit_progress = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'description', 'course', 'unit_progress', )

    def get_unit_progress(self, obj):
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
    unit_progress = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'description', 'course', 'unit_progress', )

    def get_unit_progress(self, obj):
        request = self._context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return ProgressSerializer(obj.progress.get(owner=request.user)).data
            except Exception:
                pass

class CourseDetailSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)
    progress = ProgressSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'units', 'progress',)
