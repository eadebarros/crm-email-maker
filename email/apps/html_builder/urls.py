from django.conf.urls import patterns, url
from apps.html_builder.views import *

urlpatterns = patterns('',
    url(r'^$', index.as_view(), name='index'),
    url(r'^list/$', index.as_view(), name='list'),
    url(r'^get_type/$', 'apps.html_builder.views.get_type', name='get_type'),
    url(r'^update_general_information/$', 'apps.html_builder.views.update_general_information', name='update_general_information'),
    url(r'^save_structure/$', 'apps.html_builder.views.save_structure', name='save_structure'),
    url(r'^delete_structure/$', 'apps.html_builder.views.delete_structure', name='delete_structure'),
    url(r'^edit_structure/$', 'apps.html_builder.views.edit_structure', name='edit_structure'),
    url(r'^update_order/$', 'apps.html_builder.views.update_order', name='update_order'),
    url(r'^build_html/$', 'apps.html_builder.views.build_html', name='build_html'),
    url(r'^full_structure/$', 'apps.html_builder.views.full_structure', name='full_structure'),
    url(r'^build_html_preview/$', 'apps.html_builder.views.build_html_preview', name='build_html_preview'),
)