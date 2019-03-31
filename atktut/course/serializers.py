from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from atktut.questions.models import Question
from atktut.questions.serializers import QuestionSerializer
from .models import Course, Lecture, Lesson, Progress, Unit
from drf_writable_nested import WritableNestedModelSerializer

class CourseSerializer(serializers.ModelSerializer):
    unit_count = serializers.SerializerMethodField()
    lesson_count = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'unit_count', 'lesson_count', 'hero_image', 'progress',
                  'short_description', 'objectives')

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

class ShortLessonSerializer(serializers.ModelSerializer):
    """
    A `Lesson` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'order', 'description', 'unit', 'course')

class UnitObjectSerializer(WritableNestedModelSerializer):
    def to_representation(self, value):
        if isinstance(value, Lecture):
            serializer = LectureSerializer(value)
        elif isinstance(value, Question):
            serializer = QuestionSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
        return serializer.data

    def to_internal_value(self, data):
        # you need to pass some identity to figure out which serializer to use
        # supose you'll add 'content_type' key to your json
        content_type = data.pop('content_type')

        if content_type == 'question':
            serializer = QuestionSerializer(data=data)
        elif content_type == 'lecture':
            serializer = LectureSerializer(data=data)
        else:
            raise serializers.ValidationError('no content_type provided')

        if serializer.is_valid():
            obj = serializer.save()
        else:
            raise serializers.ValidationError(serializer.errors)

        return obj

class LessonSerializer(WritableNestedModelSerializer):
    """
    A `Lesson` serializer with a `GenericRelatedField` mapping all possible
    models to their respective serializers.
    """
    unit_object = UnitObjectSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'order', 'description', 'unit',
                  'content_type', 'course', 'object_id', 'unit_object',)

    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.all(),
        slug_field='model',
    )

    # def update(self, instance, validated_data):
    #     unit_object_data = validated_data.pop('unit_object')
    #     unit_object = (instance.unit_object)

    #     instance.order = validated_data.get('order', instance.order)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.save()

    #     if instance.content_type == 'question':
    #         unit_object.content = unit_object_data.content
    #     else:
    #         unit_object.html = unit_object_data.html
    #     unit_object.save()
    #     return instance

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
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'units', 'lesson_count', 'hero_image', 'progress',
                  'short_description', 'objectives')

    def get_lesson_count(self, obj):
        return obj.lessons_course.count()

    def get_progress(self, obj):
        request = self._context.get('request')
        if request and hasattr(request, 'user'):
            try:
                return ProgressSerializer(obj.progress.get(owner=request.user)).data
            except Exception:
                pass

class UnitInfoSerializer(serializers.ModelSerializer):
    lessons = ShortLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'description', 'course')

class CourseInfoSerializer(serializers.ModelSerializer):
    units = UnitInfoSerializer(many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'units', 'hero_image', 'progress',
                  'short_description', 'objectives')

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
