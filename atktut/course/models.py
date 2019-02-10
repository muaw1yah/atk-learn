from django.db import models

# Create your models here.
class AbstractModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
         abstract = True



class Course(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return '%d: %s' % (self.id, self.name)



class Unit(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    order = models.IntegerField(unique=True)
    course = models.ForeignKey(Course, related_name='units', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.name)



class Lesson(AbstractModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    content = models.TextField()
    order = models.IntegerField(unique=True)
    unit = models.ForeignKey(Unit, related_name='lessons', on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%d: %s' % (self.order, self.name)