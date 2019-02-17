from django.db import models
from atktut.users.models import User
from atktut.commons.models import AbstractModel

# Create your models here.

class Labari(AbstractModel):
    title = models.CharField(max_length=256)
    description = models.TextField()
    keywords = models.CharField(max_length=516)
    author = models.ForeignKey(User, related_name='news', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return '%s' % (self.title)
