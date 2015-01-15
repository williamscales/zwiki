from django.conf.urls import patterns, include, url
from django.contrib import admin

from zwiki.pages import views

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index),
    url(r'^page/(?P<page_slug>[a-zA-Z0-9-]+)/$', views.page),
    url(r'^page/status/(?P<page_slug>[a-zA-Z0-9-]+)/$', views.status),
    url(r'^page/history/(?P<page_slug>[a-zA-Z0-9-]+)/$', views.page_history),
)
