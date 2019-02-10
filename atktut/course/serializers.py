from rest_framework import serializers
from .models import Course, Unit, Lesson

class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = ('id', 'name', 'content', 'order', 'unit', )


class UnitSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'course', )

class UnitDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Unit
        fields = ('id', 'name', 'order', 'lessons', 'course', )


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('id', 'name', )


class CourseDetailSerializer(serializers.ModelSerializer):
    units = UnitSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'name', 'units', )