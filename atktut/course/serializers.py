from rest_framework import serializers
from .models import Course, Unit, Lesson


class CourseSerializer(serializers.ModelSerializer):
    units = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'units', )


class UnitSerializer(serializers.ModelSerializer):
    lessons = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'course', )


class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'content', 'order', 'unit', )