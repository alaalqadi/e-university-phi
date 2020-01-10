from django import template

from tokbox.models import Student, Instructor

register = template.Library()


@register.filter(name='get_my_courses')
def get_my_courses(request, url):
    scheme = 'http'
    user_id = request.user.id
    if request.is_secure:
        scheme += 's'
    if request.user.is_authenticated:
        if request.user.userprofile.is_student:
            user_id = Student.objects.get(user_profile__user_id=user_id).id
        else:
            user_id = Instructor.objects.get(user__user_id=user_id).id
    return url + '/' + str(user_id)
