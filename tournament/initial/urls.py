from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name='list'),
    url(r'^(?P<pk>[0-9]+)/$', views.detail, name="details"),
    url(r'^(?P<pk>[0-9]+)/makefixture/$', views.makefixture, name="makefixture"),
    url(r'^(?P<pk>[0-9]+)/scoreboard/$', views.scoreboard, name="scoreboard"),
]