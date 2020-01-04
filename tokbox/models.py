from django.contrib.auth.models import AbstractUser, User
from django.db import models


class UserProfile(models.Model):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

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

    def __str__(self):
        return str(self.user_profile.user.first_name) + str(self.middle_name) + str(self.user_profile.user.last_name)


class EnrolledIn(models.Model):
    mid_grade = models.FloatField()
    final_grade = models.FloatField()
    courses = models.ForeignKey('tokbox.Course', on_delete=models.CASCADE, blank=False, null=True)
    student = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)

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

    def __str__(self):
        return str(self.user.user.first_name) + str(self.middle_name) + str(self.user.user.last_name)


class Department(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=255, blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    courses = models.ForeignKey('tokbox.Course', on_delete=models.CASCADE, blank=False, null=True)
    students = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return str(self.name) + str(self.students.objects.count())


class Faculty(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    courses = models.ForeignKey('tokbox.Course', on_delete=models.CASCADE, blank=False, null=True)
    students = models.ForeignKey('tokbox.Student', on_delete=models.CASCADE, blank=False, null=True)
    instructors = models.ForeignKey('tokbox.Instructor', on_delete=models.CASCADE, blank=False, null=True)

    def __str__(self):
        return str(self.name)
