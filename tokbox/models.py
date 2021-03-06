from datetime import timezone

from django.contrib.auth.models import AbstractUser, User
from django.db import models


class UserProfile(models.Model):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return self.user.get_full_name()


class Student(models.Model):
    middle_name = models.CharField(max_length=255, blank=False, null=False)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False)
    nationality = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    courses = models.ManyToManyField('tokbox.Course', blank=False, verbose_name='Courses', related_name="courses")
    average = models.FloatField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.user_profile.user.first_name) + str(self.middle_name) + str(self.user_profile.user.last_name)


class EnrolledIn(models.Model):
    mid_grade = models.FloatField()
    final_grade = models.FloatField()
    courses = models.ForeignKey('tokbox.Course', on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.student.user_profile.user.first_name) + str(self.courses)


class Course(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    time_start = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    DAY_OF_THE_WEEK = (
        ('SATURDAY', u'Saturday'),
        ('SUNDAY', u'Sunday'),
        ('MONDAY', u'Monday'),
        ('TUESDAY', u'Tuesday'),
        ('WEDNESDAY', u'Wednesday'),
        ('THURSDAY', u'Thursday'),
        ('FRIDAY', u'Friday'),
    )
    days = models.CharField(max_length=255, choices=DAY_OF_THE_WEEK, null=True, blank=True)
    description = models.TextField(null=True)
    what_you_will_learn = models.TextField(null=True)
    requirements = models.TextField(null=True)
    course_slides = models.FileField(upload_to='media', verbose_name="Slides", null=True)

    class Meta:
        app_label = 'tokbox'

    @property
    def get_course_instructor(self):
        return Instructor.objects.get(department__courses=self)

    @property
    def get_course_department(self):
        return Department.objects.get(courses=self)

    @property
    def get_course_duration(self):
        from datetime import datetime
        then = self.time_end
        now = datetime.now(timezone.utc)
        duration = then - now
        return duration.days

    @property
    def get_enrolled_students_number(self):
        return Student.objects.filter(courses=self).count()

    def __str__(self):
        return str(self.name) + ' - ' + str(self.time_start.date()) + ' to ' + str(self.time_end.date())


class Instructor(models.Model):
    middle_name = models.CharField(max_length=255, blank=False, null=False)
    rank = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    salary = models.FloatField()
    department = models.ForeignKey('tokbox.Department', on_delete=models.CASCADE, blank=False, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=False, null=True)
    info = models.TextField(null=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.user.user.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.user.user.last_name)


class Department(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    courses = models.ManyToManyField('tokbox.Course', blank=False, verbose_name='Courses',
                                     related_name="department_courses")
    students = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.name) + str(self.students)


class Faculty(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    courses = models.ForeignKey('tokbox.Course', on_delete=models.CASCADE, blank=False, null=True)
    students = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)
    instructors = models.ForeignKey('tokbox.Instructor', on_delete=models.CASCADE, blank=False, null=True)

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    time_start = models.DateTimeField(auto_now=False, auto_now_add=True)
    time_end = models.DateTimeField(auto_now=False, auto_now_add=False)
    description = models.CharField(max_length=255, blank=False)
    image = models.FileField(upload_to="media")

    class Meta:
        app_label = 'tokbox'

    def __str__(self):
        return str(self.name) + ' - ' + str(self.time_start.date()) + ' to ' + str(self.time_end.date())
