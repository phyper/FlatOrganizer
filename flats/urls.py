from django.conf.urls import patterns, url

from flats import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index')
)
