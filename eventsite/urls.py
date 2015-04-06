from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^events/', include('events.urls', namespace="events")),
    url(r'^admin/', include(admin.site.urls)),
)
