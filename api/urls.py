# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-7-25 上午11:36
"""

from django.conf.urls import url
from api.views import *


urlpatterns = [
    url(r'^publish_task_create/$', publish_task_create, name='publish_task_create'),
    url(r'^app_publish_task_create/$', app_publish_task_create, name='app_publish_task_create'),
    url(r'^get_projects/$', get_projects, name='get_projects'),
    url(r'^get_project_giturl/$', get_project_giturl, name='get_project_giturl'),
    url(r'^get_deploy_host/$', get_deploy_host, name='get_deploy_host'),
    url(r'^get_deploy_progress/$', get_deploy_progress, name='get_deploy_progress'),
]
