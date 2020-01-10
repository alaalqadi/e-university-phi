import logging
import os

from django.utils.safestring import mark_safe
from opentok import OpenTok
from opentok import Roles

from tokbox.models import Student, Instructor

APIKey = '46483532'
secretkey = '7317cbad70e20565914422ef80da2fd6cc3ca426'
opentok = OpenTok(APIKey, secretkey)
session = opentok.create_session()


def get_profile_type(request):
    """

    :param request:
    :return:
    """
    access_token = None
    session_id = session.session_id
    user_name = request.user.get_full_name()
    if request.user.is_authenticated:
        if request.user.userprofile.is_student:
            access_token = opentok.generate_token(session_id, role=Roles.subscriber)
        else:
            access_token = opentok.generate_token(session_id, role=Roles.publisher)
    return {'access_token': access_token, 'session_id': session_id, 'api_key': APIKey, 'user_name': user_name}
