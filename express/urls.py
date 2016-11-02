# encoding: utf-8

"""
@version: 
@author: liriqiang
@file: urls.py
@time: 16-7-19 上午10:00
"""

from django.conf.urls import url
from express.views import *


urlpatterns = [
    url(r'^project_list/$', project_list, name='project_list'),
    url(r'^project_add/$', project_add, name='project_add'),
    url(r'^project_edit/$', project_edit, name='project_edit'),
    url(r'^project_detail/$', project_detail, name='project_detail'),
    url(r'^project_del/$', project_del, name='project_del'),

    url(r'^publish_task_list/$', publish_task_list, name='publish_task_list'),
    url(r'^publish_task_detail/$', publish_task_detail, name='publish_task_detail'),
    url(r'^publish_task_trash/$', publish_task_trash, name='publish_task_trash'),
    url(r'^publish_task_deploy/$', publish_task_deploy, name='publish_task_deploy'),
    url(r'^publish_task_deploy_auto/$', publish_task_deploy_auto, name='publish_task_deploy_auto'),
    url(r'^publish_task_rollback/$', publish_task_rollback, name='publish_task_rollback'),

    url(r'^app_publish_task_list/$', app_publish_task_list, name='app_publish_task_list'),
    url(r'^app_publish_task_detail/$', app_publish_task_detail, name='app_publish_task_detail'),
    url(r'^app_publish_task_trash/$', app_publish_task_trash, name='app_publish_task_trash'),
    url(r'^app_publish_task_deploy/$', app_publish_task_deploy, name='app_publish_task_deploy'),
    url(r'^app_publish_task_rollback/$', app_publish_task_rollback, name='app_publish_task_rollback'),

    url(r'^ipa_deploy/$', ipa_deploy, name='ipa_deploy'),
]
