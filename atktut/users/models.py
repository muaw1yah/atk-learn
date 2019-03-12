import uuid
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
from django.utils.encoding import python_2_unicode_compatible
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token

from versatileimagefield.fields import VersatileImageField

def userPicture(instance, filename):
    return '/'.join(['users/avatar/', str(instance.id), filename])

@python_2_unicode_compatible
class User(AbstractUser):
    MALE = 'M'
    FEMALE = 'F'
    GENDER = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    location = models.CharField(blank=True, null=True, max_length=256)
    tagline = models.CharField(blank=True, null=True, max_length=128)
    phone = models.CharField(blank=True, null=True, max_length=64)
    email = models.CharField(blank=True, null=True, max_length=128)
    dob = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=5, choices=GENDER)
    headshot = VersatileImageField(
        'Headshot',
        upload_to=userPicture,
        null=True, blank=True
    )

    def __str__(self):
        return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
