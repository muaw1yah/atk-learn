# Generated by Django 2.1.5 on 2019-03-14 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0018_course_hero_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='objectives',
            field=models.CharField(blank=True, max_length=1028, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='short_description',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.CharField(blank=True, max_length=2056, null=True),
        ),
    ]
