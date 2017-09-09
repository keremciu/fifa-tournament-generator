from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^seasons/$', views.list, name='list'),
    url(r'^seasons/(?P<pk>[0-9]+)/$', views.detail, name="details"),
    url(r'^seasons/makefixture/(?P<pk>[0-9]+)/$', views.makefixture, name="makefixture"),
]