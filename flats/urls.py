from django.conf.urls import patterns, url
from django.contrib.auth.views import login, logout

from flats import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^(?P<flatid>\d+)/(?P<username>\w+)/$', views.profile, name='flatuser'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^password_change/', views.password_change, name='password_change'),
    url(r'^(?P<flatid>\d+)/$', views.flat, name='flat'),
    url(r'^resend_password/', views.resend_password, name='resend_password'),
)