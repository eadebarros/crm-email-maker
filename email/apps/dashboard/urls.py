from django.conf.urls import patterns, url
from apps.dashboard.views import index

urlpatterns = patterns('',
    url(r'^$', index.as_view(), name='index'),
)