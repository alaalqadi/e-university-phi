from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from tokbox.forms import CourseForm
from tokbox.models import Instructor, Student, Course, Event


@login_required
def session_view(request, course_id=None):
    course = Course.objects.get(id=course_id)
    return render(request, 'sessionScreen.html', locals())


@login_required
def home(request):
    students_count = Student.objects.all().count()
    instructors_count = Instructor.objects.all().count()
    events = Event.objects.all()
    if not request.user.is_authenticated:
        return render(reverse('account_login'))
    else:
        return render(request, 'home.html', locals())


@login_required
def courses_list(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', locals())


@login_required
def course_details(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'course_details.html', locals())


@login_required
def course_add(request):
    instance = Course()
    # if this is a POST request we need to process the form data
    # create a form instance and populate it with data from the request:
    form = CourseForm(request.POST or None, request.FILES or None, instance=instance)
    # check whether it's valid:
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('courses_list'))
    return render(request, 'course_form.html', locals())


@login_required
def course_edit(request, pk):
    instance = get_object_or_404(Course, pk=pk)
    # if this is a POST request we need to process the form data
    # create a form instance and populate it with data from the request:
    form = CourseForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('courses_list'))
    return render(request, 'course_form.html', locals())


@login_required
def instructors_list(request):
    instructors = Instructor.objects.all()
    return render(request, 'instructors.html', locals())


@login_required
def instructor_details(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk)
    return render(request, 'instructor_details.html', locals())


@login_required
def my_courses(request, pk):
    student_courses = Student.objects.filter(id=pk).values_list('courses', flat=True)
    instructor_courses = Instructor.objects.filter(id=pk).values_list('department__courses', flat=True)
    if request.user.is_authenticated:
        if request.user.userprofile.is_student:
            courses_list = Course.objects.filter(id__in=student_courses)
        else:
            courses_list = Course.objects.filter(id__in=instructor_courses)
    else:
        raise PermissionDenied
    return render(request, 'user_courses.html', locals())


def course_enrollment(request, pk):
    student = Student.objects.get(user_profile__user_id=request.user.id)
    course = Course.objects.get(id=pk)
    student.courses.add(course.id)
    return HttpResponseRedirect(reverse('my_courses', args=(student.id,)))
