# Generated by Django 2.2 on 2020-01-06 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tokbox', '0002_remove_course_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='courses',
        ),
        migrations.AddField(
            model_name='department',
            name='courses',
            field=models.ManyToManyField(null=True, to='tokbox.Course'),
        ),
    ]
