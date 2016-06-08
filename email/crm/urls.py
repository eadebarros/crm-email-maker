"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from crm import settings

# TODO: Verificar como limitar solo a usuarios que se logean, se comentan las lineas para lanzar Live
urlpatterns = [
    url(r'^', include('apps.dashboard.urls', namespace='dashboard')),
    url(r'^html_builder/', include('apps.html_builder.urls', namespace='html_builder')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
