from django.contrib.contenttypes.fields import (GenericForeignKey,
                                                GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.db import models

from atktut.config.models import AbstractModel
from atktut.users.models import User

class Course(AbstractModel):
    name = models.CharField(max_length=256)
    description = models.CharField(max_length=1028, null=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return '%s' % (self.name)

class Unit(AbstractModel):
    name = models.CharField(max_length=256)
    order = models.IntegerField(unique=True)
    description = models.CharField(blank=True, null=True, max_length=1028)
    course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course', 'order',)
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.name)

class Lesson(AbstractModel):
    name = models.CharField(max_length=256)
    order = models.IntegerField(unique=True)
    description = models.CharField(blank=True, null=True, max_length=1028)
    unit = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    unit_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = ('unit', 'order', )
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.name)

class Lecture(AbstractModel):
    content = models.TextField()
    lesson = GenericRelation(Lesson, related_query_name='lectures')

    def __str__(self):
        return '%s' % (self.lesson.content)

class Progress(AbstractModel):
    value = models.IntegerField(default=0)
    course = models.ForeignKey(Course, related_name='progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='progress',
                               on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(User, related_name='progress', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('lesson', 'owner',)
        ordering = ['created']

    def __str__(self):
        return '%d: %d' % (self.value, self.lesson)
