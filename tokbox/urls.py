from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^session_view', views.session_view, name="session_view"),
]
