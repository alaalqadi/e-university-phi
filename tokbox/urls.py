from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^courses_list', views.courses_list, name="courses_list"),
    url(r'^course_details/(\d+)/', views.course_details, name="course_details"),
    url(r'^course_add/', views.course_add, name="course_add"),
    url(r'^course_edit/(\d+)/', views.course_edit, name="course_edit"),
    url(r'^instructors_list', views.instructors_list, name="instructors_list"),
    url(r'^instructor_details/(\d+)/', views.instructor_details, name="instructor_details"),
    url(r'^my_courses/(\d+)/', views.my_courses, name="my_courses"),
    url(r'^course_enrollment/(\d+)/', views.course_enrollment, name="course_enrollment"),
    url(r'^session_view/(\d+)/', views.session_view, name="session_view"),
]
