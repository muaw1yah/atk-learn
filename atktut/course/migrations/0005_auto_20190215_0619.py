# Generated by Django 2.1.5 on 2019-02-15 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_auto_20190214_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='unit',
            name='order',
            field=models.IntegerField(),
        ),
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('unit', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='unit',
            unique_together={('course', 'order')},
        ),
    ]
