from django.conf.urls import patterns, include, url
from flats import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tasklist.views.home', name='home'),
    # url(r'^tasklist/', include('tasklist.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^flats/', include('flats.urls')),
    #url(r'^register/$', views.register, name='register'),
)
