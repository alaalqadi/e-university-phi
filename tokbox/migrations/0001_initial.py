# Generated by Django 2.2 on 2020-01-03 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('time_end', models.DateTimeField()),
                ('days', models.CharField(blank=True, choices=[('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday'), ('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday')], max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('courses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Course')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_student', models.BooleanField(default=False, verbose_name='student status')),
                ('is_teacher', models.BooleanField(default=False, verbose_name='teacher status')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('nationality', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('average', models.FloatField()),
                ('courses', models.ManyToManyField(related_name='courses', to='tokbox.Course', verbose_name='Courses')),
                ('user_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('middle_name', models.CharField(max_length=255)),
                ('rank', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('salary', models.FloatField()),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Department')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('courses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Course')),
                ('instructors', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Instructor')),
                ('students', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Student')),
            ],
        ),
        migrations.CreateModel(
            name='EnrolledIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mid_grade', models.FloatField()),
                ('final_grade', models.FloatField()),
                ('courses', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Student')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='students',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Student'),
        ),
        migrations.AddField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tokbox.Instructor'),
        ),
    ]
