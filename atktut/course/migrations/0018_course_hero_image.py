# Generated by Django 2.1.5 on 2019-02-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0017_auto_20190225_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='hero_image',
            field=models.URLField(blank=True, max_length=128, null=True),
        ),
    ]