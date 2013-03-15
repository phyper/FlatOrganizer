from django.conf.urls import patterns, url
from tasklist.settings import MEDIA_ROOT
from flats import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<flatid>\d+)/(?P<username>\w+)/$', views.profile, name='flatuser'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^(?P<flatid>\d+)/$', views.flat, name='flat'),
)

urlpatterns += patterns('',
    (r'^imgs/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': MEDIA_ROOT}))