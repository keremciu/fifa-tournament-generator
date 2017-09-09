from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^seasons/$', views.list, name='list'),
    url(r'^seasons/(?P<pk>[0-9]+)/$', views.detail, name="details"),
    url(r'^seasons/(?P<pk>[0-9]+)/makefixture/$', views.makefixture, name="makefixture"),
    url(r'^seasons/(?P<pk>[0-9]+)/scoreboard/$', views.scoreboard, name="scoreboard"),
]