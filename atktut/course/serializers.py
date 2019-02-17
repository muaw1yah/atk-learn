from rest_framework import serializers
from .models import Course, Unit, Lesson, Progress, Lecture
from generic_relations.relations import GenericRelatedField
from atktut.questions.models import Question
from atktut.questions.serializers import QuestionSerializer


class CourseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Course
        fields = ('id', 'name', 'description', )


class UnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'description', 'course', )


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
    })
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'order', 'description', 'unit', 'unit_object', )


class UnitDetailSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False, read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'description', 'course', )


class CourseDetailSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'description', 'units', )


class ProgressSerializer(serializers.ModelSerializer):
    course = CourseDetailSerializer(many=False, read_only=True)

    class Meta:
        model = Progress
        fields = ('value', 'course', )