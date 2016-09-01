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
]
