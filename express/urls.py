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
    url(r'^express_list/$', express_list, name='express_list'),
    url(r'^express_add/$', express_add, name='express_add'),
    url(r'^express_detail/$', express_detail, name='express_detail'),

    url(r'^express_app_list/$', express_app_list, name='express_app_list'),
]
