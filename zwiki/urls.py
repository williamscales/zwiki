from django.conf.urls import patterns, include, url
from django.contrib import admin

from zwiki.pages import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^(?P<page_slug>[a-zA-Z0-9-]+)/$', views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
