"""UnifiedIT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from Accountant import views
from Profiler.admin import institute_admin_site
from Accountant.admin import main_admin

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^accountant/', include('Accountant.urls')),
    url(r'^admin/', main_admin.urls, name='main_admin'),
    url(r'^institute_admin/', institute_admin_site.urls, name='institute_admin')
]
