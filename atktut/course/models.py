from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from atktut.config.models import AbstractModel
from atktut.users.models import User


class Course(AbstractModel):
    name = models.CharField(max_length=256)
    short_description = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=2056, null=True, blank=True)
    hero_image = models.URLField(max_length=128, null=True, blank=True)
    objectives = models.CharField(max_length=1028, null=True, blank=True)

    class Meta:
        ordering = ['created']

class Unit(AbstractModel):
    name = models.CharField(max_length=256)
    order = models.IntegerField()
    description = models.CharField(blank=True, null=True, max_length=1028)
    course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'order',)
        ordering = ['order']

class Lesson(AbstractModel):
    name = models.CharField(max_length=256)
    order = models.IntegerField()
    description = models.CharField(blank=True, null=True, max_length=1028)
    unit = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='lessons_course',
                               on_delete=models.CASCADE, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    unit_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('unit', 'order', )
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.name)

    def to_representation(self, obj):
        return obj.model

    def to_internal_value(self, data):
        return ContentType.objects.get(model=data)

class Lecture(AbstractModel):
    HTML = 'HTML'
    VIDEO = 'VID'
    PICTURE = 'PIC'
    LECTURE_TYPE = (
        (HTML, 'HTML'),
        (VIDEO, 'Video'),
        (PICTURE, 'Picture'),
    )
    lecture_type = models.CharField(default=HTML, max_length=5, choices=LECTURE_TYPE)
    html = models.TextField(blank=True, null=True)
    video = models.CharField(blank=True, null=True, max_length=128)
    picture = models.URLField(blank=True, null=True)
    lesson = GenericRelation(Lesson, related_query_name='lectures')

    def __str__(self):
        return '%d %s' % (self.pk, self.lecture_type)

    def to_representation(self, obj):
        return obj.model

    def to_internal_value(self, data):
        return ContentType.objects.get(model=data)

class Progress(AbstractModel):
    total_lessons = models.IntegerField(default=0)
    lesson = models.ForeignKey(Lesson, related_name='progress',
                               on_delete=models.CASCADE, blank=True, null=True)
    unit = models.ForeignKey(Unit, related_name='progress', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, related_name='progress_lessons')
    completed_units = models.ManyToManyField(Unit, related_name='progress_units')

    class Meta:
        unique_together = ('course', 'owner',)
        ordering = ['created']
